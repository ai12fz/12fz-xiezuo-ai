"""LangGraph tool adapter for 12FZ协作AI tool integration.

This module contains the LangGraphToolAdapter class that converts 12FZ协作AI tools
to LangGraph-compatible format using langchain_core.tools.
"""

from collections.abc import Awaitable
import inspect
from typing import Any

from fzxiezuoai.agents.agent_adapters.base_tool_adapter import BaseToolAdapter
from fzxiezuoai.tools.base_tool import BaseTool


class LangGraphToolAdapter(BaseToolAdapter):
    """Adapts 12FZ协作AI tools to LangGraph agent tool compatible format.

    Converts 12FZ协作AI BaseTool instances to langchain_core.tools format
    that can be used by LangGraph agents.
    """

    def __init__(self, tools: list[BaseTool] | None = None) -> None:
        """Initialize the tool adapter.

        Args:
            tools: Optional list of 12FZ协作AI tools to adapt.
        """
        super().__init__()
        self.original_tools: list[BaseTool] = tools or []
        self.converted_tools: list[Any] = []

    def configure_tools(self, tools: list[BaseTool]) -> None:
        """Configure and convert 12FZ协作AI tools to LangGraph-compatible format.

        LangGraph expects tools in langchain_core.tools format. This method
        converts 12FZ协作AI BaseTool instances to StructuredTool instances.

        Args:
            tools: List of 12FZ协作AI tools to convert.
        """
        from langchain_core.tools import BaseTool as LangChainBaseTool, StructuredTool

        converted_tools: list[Any] = []
        if self.original_tools:
            all_tools: list[BaseTool] = tools + self.original_tools
        else:
            all_tools = tools
        for tool in all_tools:
            if isinstance(tool, LangChainBaseTool):
                converted_tools.append(tool)
                continue

            sanitized_name: str = self.sanitize_tool_name(tool.name)

            async def tool_wrapper(
                *args: Any, tool: BaseTool = tool, **kwargs: Any
            ) -> Any:
                """Wrapper function to adapt 12FZ协作AI tool calls to LangGraph format.

                Args:
                    *args: Positional arguments for the tool.
                    tool: The 12FZ协作AI tool to wrap.
                    **kwargs: Keyword arguments for the tool.

                Returns:
                    The result from the tool execution.
                """
                output: Any | Awaitable[Any]
                if len(args) > 0 and isinstance(args[0], str):
                    output = tool.run(args[0])
                elif "input" in kwargs:
                    output = tool.run(kwargs["input"])
                else:
                    output = tool.run(**kwargs)

                if inspect.isawaitable(output):
                    result: Any = await output
                else:
                    result = output
                return result

            converted_tool: StructuredTool = StructuredTool(
                name=sanitized_name,
                description=tool.description,
                func=tool_wrapper,
                args_schema=tool.args_schema,
            )

            converted_tools.append(converted_tool)

        self.converted_tools = converted_tools

    def tools(self) -> list[Any]:
        """Get the list of converted tools.

        Returns:
            List of LangGraph-compatible tools.
        """
        return self.converted_tools or []
