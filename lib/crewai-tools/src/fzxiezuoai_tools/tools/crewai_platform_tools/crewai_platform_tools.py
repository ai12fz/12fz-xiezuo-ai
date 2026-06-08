import logging

from fzxiezuoai.tools import BaseTool

from fzxiezuoai_tools.adapters.tool_collection import ToolCollection
from fzxiezuoai_tools.tools.crewai_platform_tools.crewai_platform_tool_builder import (
    CrewaiPlatformToolBuilder,
)


logger = logging.getLogger(__name__)


def CrewaiPlatformTools(  # noqa: N802
    apps: list[str],
) -> ToolCollection[BaseTool]:
    """Factory function that returns fzxiezuoai platform tools.

    Args:
        apps: List of platform apps to get tools that are available on the platform.

    Returns:
        A list of BaseTool instances for platform actions
    """
    builder = CrewaiPlatformToolBuilder(apps=apps)

    return builder.tools()  # type: ignore
