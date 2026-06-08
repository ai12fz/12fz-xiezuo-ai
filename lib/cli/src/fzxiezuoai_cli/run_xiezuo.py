from enum import Enum
import subprocess

import click
from fzxiezuoai_core.constants import CREWAI_TRAINED_AGENTS_FILE_ENV
from packaging import version

from fzxiezuoai_cli.utils import build_env_with_all_tool_credentials, read_toml
from fzxiezuoai_cli.version import get_fzxiezuoai_version


class XiezuoType(Enum):
    STANDARD = "standard"
    FLOW = "flow"


def run_xiezuo(trained_agents_file: str | None = None) -> None:
    """Run the xiezuo or flow by running a command in the UV environment.

    Starting from version 0.103.0, this command can be used to run both
    standard xiezuos and flows. For flows, it detects the type from pyproject.toml
    and automatically runs the appropriate command.

    Args:
        trained_agents_file: Optional path to a trained-agents pickle produced
            by ``fzxiezuoai train -f``. When set, exported as
            ``CREWAI_TRAINED_AGENTS_FILE`` so agents load suggestions from this
            file instead of the default ``trained_agents_data.pkl``.
    """
    fzxiezuoai_version = get_fzxiezuoai_version()
    min_required_version = "0.71.0"
    pyproject_data = read_toml()

    if pyproject_data.get("tool", {}).get("poetry") and (
        version.parse(fzxiezuoai_version) < version.parse(min_required_version)
    ):
        click.secho(
            f"You are running an older version of 12FZ协作AI ({fzxiezuoai_version}) that uses poetry pyproject.toml. "
            f"Please run `fzxiezuoai update` to update your pyproject.toml to use uv.",
            fg="red",
        )

    is_flow = pyproject_data.get("tool", {}).get("fzxiezuoai", {}).get("type") == "flow"
    xiezuo_type = XiezuoType.FLOW if is_flow else XiezuoType.STANDARD

    click.echo(f"Running the {'Flow' if is_flow else 'Xiezuo'}")

    execute_command(xiezuo_type, trained_agents_file=trained_agents_file)


def execute_command(
    xiezuo_type: XiezuoType, trained_agents_file: str | None = None
) -> None:
    """Execute the appropriate command based on xiezuo type.

    Args:
        xiezuo_type: The type of xiezuo to run.
        trained_agents_file: Optional trained-agents pickle path forwarded to
            the subprocess via the ``CREWAI_TRAINED_AGENTS_FILE`` env var.
    """
    command = ["uv", "run", "kickoff" if xiezuo_type == XiezuoType.FLOW else "run_xiezuo"]

    env = build_env_with_all_tool_credentials()
    if trained_agents_file:
        env[CREWAI_TRAINED_AGENTS_FILE_ENV] = trained_agents_file

    try:
        subprocess.run(command, capture_output=False, text=True, check=True, env=env)  # noqa: S603

    except subprocess.CalledProcessError as e:
        handle_error(e, xiezuo_type)

    except Exception as e:
        click.echo(f"An unexpected error occurred: {e}", err=True)


def handle_error(error: subprocess.CalledProcessError, xiezuo_type: XiezuoType) -> None:
    """
    Handle subprocess errors with appropriate messaging.

    Args:
        error: The subprocess error that occurred
        xiezuo_type: The type of xiezuo that was being run
    """
    entity_type = "flow" if xiezuo_type == XiezuoType.FLOW else "xiezuo"
    click.echo(f"An error occurred while running the {entity_type}: {error}", err=True)

    if error.output:
        click.echo(error.output, err=True, nl=True)

    pyproject_data = read_toml()
    if pyproject_data.get("tool", {}).get("poetry"):
        click.secho(
            "It's possible that you are using an old version of 12FZ协作AI that uses poetry, "
            "please run `fzxiezuoai update` to update your pyproject.toml to use uv.",
            fg="yellow",
        )
