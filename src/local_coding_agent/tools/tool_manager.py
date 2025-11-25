"""
Manages the registration and execution of tools available to the agent.
"""

from typing import Any, Callable, Dict, List


class ToolManager:
    """A class to manage and execute tools."""

    def __init__(self):
        self._tools: Dict[str, Callable[..., Any]] = {}
        self._tool_schemas: List[Dict[str, Any]] = []

    def register_tool(self, func: Callable[..., Any], schema: Dict[str, Any]):
        """
        Register a tool for the agent to use.

        Args:
            func: The function to be executed.
            schema: The schema describing the tool for the LLM.
        """
        tool_name = schema.get("function", {}).get("name")
        if not tool_name:
            raise ValueError("Tool schema must have a 'function.name' key.")

        self._tools[tool_name] = func
        self._tool_schemas.append(schema)

    def get_tool_schemas(self) -> List[Dict[str, Any]]:
        """Return the list of schemas for all registered tools."""
        return self._tool_schemas

    def execute_tool(self, tool_name: str, **kwargs: Any) -> Any:
        """
        Execute a registered tool.

        Args:
            tool_name: The name of the tool to execute.
            **kwargs: The arguments to pass to the tool.

        Returns:
            The result of the tool's execution.
        
        Raises:
            ValueError: If the tool is not found.
        """
        if tool_name not in self._tools:
            raise ValueError(f"Tool '{tool_name}' not found.")
        return self._tools[tool_name](**kwargs)
