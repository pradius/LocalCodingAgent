"""
Unit tests for the ToolManager class.
"""

import pytest
from local_coding_agent.tools.tool_manager import ToolManager

# A simple tool for testing
def sample_tool(param1: str, param2: int) -> str:
    """A sample tool for testing purposes."""
    return f"{param1} - {param2}"


SAMPLE_SCHEMA = {
    "type": "function",
    "function": {
        "name": "sample_tool",
        "description": "A sample tool for testing.",
        "parameters": {
            "type": "object",
            "properties": {
                "param1": {"type": "string"},
                "param2": {"type": "integer"},
            },
            "required": ["param1", "param2"],
        },
    },
}


@pytest.fixture
def tool_manager():
    """Provides a ToolManager instance for testing."""
    return ToolManager()


def test_register_tool_success(tool_manager: ToolManager):
    """Test successful registration of a tool."""
    tool_manager.register_tool(sample_tool, SAMPLE_SCHEMA)
    schemas = tool_manager.get_tool_schemas()
    assert len(schemas) == 1
    assert schemas[0] == SAMPLE_SCHEMA
    assert "sample_tool" in tool_manager._tools


def test_register_tool_invalid_schema(tool_manager: ToolManager):
    """Test registration with an invalid schema (missing name)."""
    invalid_schema = {"type": "function"}  # Missing 'function' key
    with pytest.raises(ValueError, match="Tool schema must have a 'function.name' key."):
        tool_manager.register_tool(sample_tool, invalid_schema)


def test_execute_tool_success(tool_manager: ToolManager):
    """Test successful execution of a registered tool."""
    tool_manager.register_tool(sample_tool, SAMPLE_SCHEMA)
    result = tool_manager.execute_tool("sample_tool", param1="test", param2=123)
    assert result == "test - 123"


def test_execute_tool_not_found(tool_manager: ToolManager):
    """Test execution of a non-existent tool."""
    with pytest.raises(ValueError, match="Tool 'non_existent_tool' not found."):
        tool_manager.execute_tool("non_existent_tool")


def test_get_tool_schemas_empty(tool_manager: ToolManager):
    """Test that get_tool_schemas returns an empty list initially."""
    assert tool_manager.get_tool_schemas() == []


def test_register_multiple_tools(tool_manager: ToolManager):
    """Test registering multiple tools."""
    schema2 = SAMPLE_SCHEMA.copy()
    schema2["function"]["name"] = "sample_tool_2"
    
    tool_manager.register_tool(sample_tool, SAMPLE_SCHEMA)
    tool_manager.register_tool(lambda: "tool2", schema2)

    schemas = tool_manager.get_tool_schemas()
    assert len(schemas) == 2
    assert "sample_tool" in tool_manager._tools
    assert "sample_tool_2" in tool_manager._tools

