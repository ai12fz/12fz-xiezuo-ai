"""Interactive chat interface for 12FZ协作AI crews — chat.12fz.com edition.

Replaces the original terminal-based chat with WebSocket connection
to our own chat.12fz.com infrastructure.
"""
from __future__ import annotations

import contextvars
import json
import os
import platform
import re
import sys
import threading
import time
from pathlib import Path
from typing import Any, Final, Literal

import click
import httpx
from fzxiezuoai_core.printer import PRINTER
from packaging import version
import tomli

from fzxiezuoai.crew import Crew
from fzxiezuoai.llm import LLM
from fzxiezuoai.llms.base_llm import BaseLLM
from fzxiezuoai.types.crew_chat import ChatInputField, ChatInputs
from fzxiezuoai.utilities.llm_utils import create_llm
from fzxiezuoai.utilities.project_utils import read_toml
from fzxiezuoai.utilities.types import LLMMessage
from fzxiezuoai.version import get_fzxiezuoai_version

MIN_REQUIRED_VERSION: Final[Literal["0.98.0"]] = "0.98.0"

DEFAULT_INPUT_DESCRIPTION: Final[str] = "Input value for the crew's tasks and agents."
DEFAULT_CREW_DESCRIPTION: Final[str] = "A 12FZ协作AI crew."

CHAT_HOST = os.environ.get("FZXIEZUOAI_CHAT_HOST", "chat.12fz.com")
HTTP_PROTO = "https"
WS_PROTO = "wss"

# Mapping of known bot IDs to their tokens
# Users can override via FZXIEZUOAI_BOT_TOKEN env var
FALLBACK_TOKENS = {
    "chaogu-ai": "chat-token-chaogu-2026",
    "高级工程师": "chat-token-senior-2026",
    "服务器技术": "chat-token-server-2026",
    "gong3": "chat-token-gong3-2026",
}


def _get_bot_token(bot_id: str) -> str:
    """Get bot token from env var or fallback list."""
    if token := os.environ.get("FZXIEZUOAI_BOT_TOKEN"):
        return token
    if token := FALLBACK_TOKENS.get(bot_id):
        return token
    # Generate a deterministic token based on bot_id for local dev
    return f"12fz-{bot_id}-token"


def run_chat() -> None:
    """Start a chat.12fz.com interactive session for the current crew.

    Connects to chat.12fz.com via WebSocket, creates a group for the crew,
    and responds to messages using the crew's chat LLM.
    """
    crewai_version = get_fzxiezuoai_version()
    pyproject_data = read_toml()

    if not check_conversational_crews_version(crewai_version, pyproject_data):
        return

    crew, crew_name = load_crew_and_name()
    chat_llm = initialize_chat_llm(crew)
    if not chat_llm:
        return

    # Generate bot identity
    bot_id = f"crew-{crew_name.lower().replace('_', '-')}"

    click.secho(
        f"\nConnecting {bot_id} to {CHAT_HOST} ...",
        fg="white",
    )

    # Analyze crew and prepare chat
    click.secho(
        "\nAnalyzing crew and required inputs ...",
        fg="white",
    )
    loading_complete = threading.Event()
    ctx = contextvars.copy_context()
    loading_thread = threading.Thread(
        target=ctx.run, args=(show_loading, loading_complete)
    )
    loading_thread.start()

    try:
        crew_chat_inputs = generate_crew_chat_inputs(crew, crew_name, chat_llm)
        crew_tool_schema = generate_crew_tool_schema(crew_chat_inputs)
        system_message = build_system_message(crew_chat_inputs)
    finally:
        loading_complete.set()
        loading_thread.join()

    click.secho("\nFinished analyzing crew.\n", fg="white")

    # Now connect to chat.12fz.com
    token = _get_bot_token(bot_id)
    ws_url = f"{WS_PROTO}://{CHAT_HOST}/ws?token={token}"
    api_base = f"{HTTP_PROTO}://{CHAT_HOST}"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}",
    }

    # Create a group for this crew
    group_name = f"Xiezuo: {crew_name}"
    group_id = _create_or_join_group(api_base, headers, group_name)
    if group_id is None:
        click.secho("Failed to create/join group. Exiting.", fg="red")
        sys.exit(1)

    click.secho(f"✅ Crew '{crew_name}' is online!", fg="green")
    click.secho(f"   Group ID: {group_id}", fg="white")
    click.secho(f"   Bot ID:   {bot_id}", fg="white")
    click.secho(f"   Server:   {CHAT_HOST}", fg="white")
    click.secho("")
    click.secho("Send messages to this group on chat.12fz.com", fg="blue")
    click.secho("Press Ctrl+C to stop.\n", fg="yellow")

    # Send welcome message
    messages: list[LLMMessage] = [
        {"role": "system", "content": system_message},
    ]
    _send_message(api_base, headers, group_id, f"🤖 **{crew_name}** is now online! Send me a message to get started.")

    available_functions = {
        crew_chat_inputs.crew_name: _make_tool_function(crew, messages),
    }

    # Connect WebSocket and enter event loop
    _start_ws_loop(
        ws_url=ws_url,
        headers=headers,
        api_base=api_base,
        group_id=group_id,
        bot_id=bot_id,
        chat_llm=chat_llm,
        messages=messages,
        crew_tool_schema=crew_tool_schema,
        available_functions=available_functions,
    )


def _create_or_join_group(api_base: str, headers: dict, name: str) -> int | None:
    """Find an existing group by name, or create a new one."""
    try:
        # List existing groups
        resp = httpx.get(f"{api_base}/api/groups", headers=headers, timeout=10)
        if resp.status_code == 200:
            groups = resp.json()
            if isinstance(groups, list):
                for g in groups:
                    if g.get("name") == name:
                        return g["id"]

        # Create new group
        resp = httpx.post(
            f"{api_base}/api/groups",
            headers=headers,
            json={"name": name},
            timeout=10,
        )
        if resp.status_code in (200, 201):
            return resp.json()["id"]
        click.secho(f"Create group failed: {resp.status_code} {resp.text}", fg="red")
    except Exception as e:
        click.secho(f"Group error: {e}", fg="red")
    return None


def _send_message(api_base: str, headers: dict, group_id: int, content: str) -> None:
    """Send a message to a group via the REST API."""
    try:
        httpx.post(
            f"{api_base}/api/messages",
            headers=headers,
            json={"group_id": group_id, "content": content},
            timeout=10,
        )
    except Exception:
        pass


def _make_tool_function(crew: Crew, messages: list[LLMMessage]) -> Any:
    """Create a wrapper function for running the crew tool."""
    def run_crew_tool_with_messages(**kwargs: Any) -> str:
        return _run_crew_tool(crew, messages, **kwargs)
    return run_crew_tool_with_messages


def _run_crew_tool(crew: Crew, messages: list[LLMMessage], **kwargs: Any) -> str:
    """Run the crew with the given inputs."""
    try:
        kwargs["crew_chat_messages"] = json.dumps(messages)
        crew_output = crew.kickoff(inputs=kwargs)
        return str(crew_output)
    except Exception as e:
        return f"Error: {e}"


def _start_ws_loop(
    ws_url: str,
    headers: dict,
    api_base: str,
    group_id: int,
    bot_id: str,
    chat_llm: LLM | BaseLLM,
    messages: list[LLMMessage],
    crew_tool_schema: dict[str, Any],
    available_functions: dict[str, Any],
) -> None:
    """WebSocket event loop — listen for messages, respond via chat LLM."""
    try:
        import websocket as ws_lib
    except ImportError:
        click.secho(
            "The 'websocket-client' package is required. Install with: pip install websocket-client",
            fg="red",
        )
        sys.exit(1)

    def on_message(ws, raw):
        try:
            msg = json.loads(raw)
            if msg.get("type") != "message":
                return
            data = msg.get("data", {})
            sender = data.get("sender_id", "")
            content = data.get("content", "")
            msg_group_id = data.get("group_id")

            # Skip our own messages and messages from other groups
            if sender == bot_id:
                return
            if msg_group_id != group_id:
                return

            click.echo(f"[{sender}] {content[:80]}")

            # Check if we're mentioned
            mentioned = f"@{bot_id}" in content or f"@{bot_id}" in content.replace("crew-", "")

            if not mentioned:
                return

            # Remove @mention from content
            user_msg = re.sub(rf"@\S*{re.escape(bot_id)}\S*", "", content).strip()
            if not user_msg:
                user_msg = content

            click.echo(f"Processing: {user_msg[:60]}...")

            # Add user message to history
            messages.append({"role": "user", "content": user_msg})

            # Get response from chat LLM
            response = chat_llm.call(
                messages=messages,
                tools=[crew_tool_schema],
                available_functions=available_functions,
            )

            messages.append({"role": "assistant", "content": response})

            # Send reply back to chat
            _send_message(api_base, headers, msg_group_id, response)

        except Exception as e:
            click.secho(f"WS error: {e}", fg="red")

    def on_error(ws, error):
        click.secho(f"WS error: {error}", fg="red")

    def on_close(ws, close_status_code, close_msg):
        click.echo("WebSocket closed. Reconnecting in 5s...")

    def on_open(ws):
        click.echo("WebSocket connected. Waiting for messages...")

    ws_app = ws_lib.WebSocketApp(
        ws_url,
        on_message=on_message,
        on_error=on_error,
        on_close=on_close,
        on_open=on_open,
    )

    try:
        ws_app.run_forever(ping_interval=30, ping_timeout=10)
    except KeyboardInterrupt:
        click.echo("\nShutting down...")
        _send_message(api_base, headers, group_id, f"👋 **{bot_id}** going offline.")
    except Exception as e:
        click.secho(f"Connection error: {e}", fg="red")


# ======== Existing helper functions below (unchanged) ========


def check_conversational_crews_version(
    crewai_version: str, pyproject_data: dict[str, Any]
) -> bool:
    try:
        if version.parse(crewai_version) < version.parse(MIN_REQUIRED_VERSION):
            click.secho(
                "You are using an older version of 12FZ协作AI that doesn't support conversational crews. "
                "Run 'uv upgrade fzxiezuoai' to get the latest version.",
                fg="red",
            )
            return False
    except version.InvalidVersion:
        click.secho("Invalid 12FZ协作AI version format detected.", fg="red")
        return False
    return True


def show_loading(event: threading.Event) -> None:
    while not event.is_set():
        PRINTER.print(".", end="")
        time.sleep(1)
    PRINTER.print("")


def initialize_chat_llm(crew: Crew) -> LLM | BaseLLM | None:
    try:
        return create_llm(crew.chat_llm)
    except Exception as e:
        click.secho(
            f"Unable to find a Chat LLM. Please make sure you set chat_llm on the crew: {e}",
            fg="red",
        )
        return None


def build_system_message(crew_chat_inputs: ChatInputs) -> str:
    required_fields_str = (
        ", ".join(
            f"{field.name} (desc: {field.description or 'n/a'})"
            for field in crew_chat_inputs.inputs
        )
        or "(No required fields detected)"
    )
    return (
        "You are a helpful AI assistant for the 12FZ协作AI platform. "
        "Your primary purpose is to assist users with the crew's specific tasks. "
        "You can answer general questions, but should guide users back to the crew's purpose afterward. "
        "For example, after answering a general question, remind the user of your main purpose. "
        f"Those required inputs are: {required_fields_str}. "
        "Once you have them, call the function. "
        "Please keep your responses concise and friendly. "
        "If a user asks a question outside the crew's scope, provide a brief answer and remind them of the crew's purpose. "
        "If you are ever unsure about a user's request or need clarification, ask the user for more information. "
        "Before doing anything else, introduce yourself with a friendly message."
        f"\\nCrew Name: {crew_chat_inputs.crew_name}"
        f"\\nCrew Description: {crew_chat_inputs.crew_description}"
    )


def generate_crew_tool_schema(crew_inputs: ChatInputs) -> dict[str, Any]:
    properties = {}
    for field in crew_inputs.inputs:
        properties[field.name] = {
            "type": "string",
            "description": field.description or "No description provided",
        }
    required_fields = [field.name for field in crew_inputs.inputs]
    return {
        "type": "function",
        "function": {
            "name": crew_inputs.crew_name,
            "description": crew_inputs.crew_description or "No crew description",
            "parameters": {
                "type": "object",
                "properties": properties,
                "required": required_fields,
            },
        },
    }


def load_crew_and_name() -> tuple[Crew, str]:
    cwd = Path.cwd()
    pyproject_path = cwd / "pyproject.toml"
    if not pyproject_path.exists():
        raise FileNotFoundError("pyproject.toml not found in the current directory.")
    with pyproject_path.open("rb") as f:
        pyproject_data = tomli.load(f)
    project_name = pyproject_data["project"]["name"]
    folder_name = project_name
    crew_class_name = project_name.replace("_", " ").title().replace(" ", "")
    src_path = cwd / "src"
    if str(src_path) not in sys.path:
        sys.path.insert(0, str(src_path))
    crew_module_name = f"{folder_name}.crew"
    try:
        crew_module = __import__(crew_module_name, fromlist=[crew_class_name])
    except ImportError as e:
        raise ImportError(f"Failed to import crew module {crew_module_name}: {e}") from e
    try:
        crew_class = getattr(crew_module, crew_class_name)
    except AttributeError as e:
        raise AttributeError(f"Crew class {crew_class_name} not found in module {crew_module_name}") from e
    crew_instance = crew_class().crew()
    return crew_instance, crew_class_name


def generate_crew_chat_inputs(
    crew: Crew,
    crew_name: str,
    chat_llm: LLM | BaseLLM,
    generate_descriptions: bool = True,
) -> ChatInputs:
    required_inputs = fetch_required_inputs(crew)
    input_fields = []
    for input_name in required_inputs:
        if generate_descriptions:
            description = generate_input_description_with_ai(input_name, crew, chat_llm)
        else:
            description = DEFAULT_INPUT_DESCRIPTION
        input_fields.append(ChatInputField(name=input_name, description=description))
    if generate_descriptions:
        crew_description = generate_crew_description_with_ai(crew, chat_llm)
    else:
        crew_description = DEFAULT_CREW_DESCRIPTION
    return ChatInputs(
        crew_name=crew_name, crew_description=crew_description, inputs=input_fields
    )


def fetch_required_inputs(crew: Crew) -> set[str]:
    return crew.fetch_inputs()


def generate_input_description_with_ai(
    input_name: str, crew: Crew, chat_llm: LLM | BaseLLM
) -> str:
    context_texts = []
    placeholder_pattern = re.compile(r"{(.+?)}")
    for task in crew.tasks:
        if (
            f"{{{input_name}}}" in task.description
            or f"{{{input_name}}}" in task.expected_output
        ):
            task_description = placeholder_pattern.sub(
                lambda m: m.group(1), task.description or ""
            )
            expected_output = placeholder_pattern.sub(
                lambda m: m.group(1), task.expected_output or ""
            )
            context_texts.append(f"Task Description: {task_description}")
            context_texts.append(f"Expected Output: {expected_output}")
    for agent in crew.agents:
        if (
            f"{{{input_name}}}" in agent.role
            or f"{{{input_name}}}" in agent.goal
            or f"{{{input_name}}}" in agent.backstory
        ):
            agent_role = placeholder_pattern.sub(lambda m: m.group(1), agent.role or "")
            agent_goal = placeholder_pattern.sub(lambda m: m.group(1), agent.goal or "")
            agent_backstory = placeholder_pattern.sub(
                lambda m: m.group(1), agent.backstory or ""
            )
            context_texts.append(f"Agent Role: {agent_role}")
            context_texts.append(f"Agent Goal: {agent_goal}")
            context_texts.append(f"Agent Backstory: {agent_backstory}")
    context = "\n".join(context_texts)
    if not context:
        raise ValueError(f"No context found for input '{input_name}'.")
    prompt = (
        f"Based on the following context, write a concise description (15 words or less) of the input '{input_name}'.\\n"
        "Provide only the description, without any extra text or labels. Do not include placeholders like '{topic}' in the description.\\n"
        f"Context:\\n{context}"
    )
    try:
        response = chat_llm.call(messages=[{"role": "user", "content": prompt}])
    except Exception as exc:
        click.secho(
            f"Warning: failed to generate input description for '{input_name}' ({exc}); using default.",
            fg="yellow",
        )
        return DEFAULT_INPUT_DESCRIPTION
    return str(response).strip()


def generate_crew_description_with_ai(crew: Crew, chat_llm: LLM | BaseLLM) -> str:
    context_texts = []
    placeholder_pattern = re.compile(r"{(.+?)}")
    for task in crew.tasks:
        task_description = placeholder_pattern.sub(
            lambda m: m.group(1), task.description or ""
        )
        expected_output = placeholder_pattern.sub(
            lambda m: m.group(1), task.expected_output or ""
        )
        context_texts.append(f"Task Description: {task_description}")
        context_texts.append(f"Expected Output: {expected_output}")
    for agent in crew.agents:
        agent_role = placeholder_pattern.sub(lambda m: m.group(1), agent.role or "")
        agent_goal = placeholder_pattern.sub(lambda m: m.group(1), agent.goal or "")
        agent_backstory = placeholder_pattern.sub(
            lambda m: m.group(1), agent.backstory or ""
        )
        context_texts.append(f"Agent Role: {agent_role}")
        context_texts.append(f"Agent Goal: {agent_goal}")
        context_texts.append(f"Agent Backstory: {agent_backstory}")
    context = "\n".join(context_texts)
    prompt = (
        "Based on the following context, write a concise description (15 words or less) "
        "of the crew's purpose. Provide only the description, without any extra text or labels.\\n"
        f"Context:\\n{context}"
    )
    try:
        response = chat_llm.call(messages=[{"role": "user", "content": prompt}])
    except Exception as exc:
        click.secho(
            f"Warning: failed to generate crew description ({exc}); using default.",
            fg="yellow",
        )
        return DEFAULT_CREW_DESCRIPTION
    return str(response).strip()
