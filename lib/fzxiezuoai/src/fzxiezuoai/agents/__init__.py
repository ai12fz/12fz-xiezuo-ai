from typing import TYPE_CHECKING, Any

from fzxiezuoai.agents.cache.cache_handler import CacheHandler
from fzxiezuoai.agents.parser import AgentAction, AgentFinish, OutputParserError, parse
from fzxiezuoai.agents.tools_handler import ToolsHandler


if TYPE_CHECKING:
    from fzxiezuoai.agents.crew_agent_executor import CrewAgentExecutor


__all__ = [
    "AgentAction",
    "AgentFinish",
    "CacheHandler",
    "CrewAgentExecutor",
    "OutputParserError",
    "ToolsHandler",
    "parse",
]


def __getattr__(name: str) -> Any:
    if name == "CrewAgentExecutor":
        from fzxiezuoai.agents.crew_agent_executor import CrewAgentExecutor

        return CrewAgentExecutor
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
