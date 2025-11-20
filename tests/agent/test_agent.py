"""
Unit tests for the CodingAgent class.
"""

from unittest.mock import MagicMock
import pytest
from local_coding_agent.agent.agent import CodingAgent
from local_coding_agent.llm.llm_provider import LLMProvider
from local_coding_agent.tools.tool_manager import ToolManager


@pytest.fixture
def mock_llm_provider():
    """Provides a mock LLMProvider."""
    return MagicMock(spec=LLMProvider)


@pytest.fixture
def mock_tool_manager():
    """Provides a mock ToolManager."""
    return MagicMock(spec=ToolManager)


@pytest.fixture
def coding_agent(mock_llm_provider, mock_tool_manager):
    """Provides a CodingAgent instance with mock dependencies."""
    return CodingAgent(llm_provider=mock_llm_provider, tool_manager=mock_tool_manager)


def test_agent_chooses_tool(coding_agent, mock_llm_provider, mock_tool_manager):
    """Test that the agent correctly identifies and executes a tool."""
    user_prompt = "Read the file 'test.py'"
    tool_schemas = [{"name": "read_file"}]
    tool_call = {"tool_name": "read_file", "arguments": {"file_path": "test.py"}}
    tool_result = "file content"

    mock_tool_manager.get_tool_schemas.return_value = tool_schemas
    mock_llm_provider.get_tool_usage.return_value = tool_call
    mock_tool_manager.execute_tool.return_value = tool_result

    response = coding_agent.run_interaction(user_prompt)

    # Verify that the LLM was asked to decide on a tool
    mock_llm_provider.get_tool_usage.assert_called_once_with(user_prompt, tool_schemas)

    # Verify that the correct tool was executed
    mock_tool_manager.execute_tool.assert_called_once_with(
        tool_name="read_file", file_path="test.py"
    )

    # Verify the final response is the tool's result
    assert response == tool_result

    # Verify that a direct response was not generated
    mock_llm_provider.get_response.assert_not_called()

    # Verify conversation history
    assert len(coding_agent.conversation_history) == 2
    assert coding_agent.conversation_history[0] == {"role": "user", "content": user_prompt}
    assert coding_agent.conversation_history[1] == {"role": "assistant", "content": tool_result}


def test_agent_generates_direct_response(coding_agent, mock_llm_provider, mock_tool_manager):
    """Test that the agent generates a direct response when no tool is needed."""
    user_prompt = "What is the meaning of life?"
    direct_response = "42"

    # Simulate the LLM deciding not to use a tool
    mock_llm_provider.get_tool_usage.return_value = None
    mock_llm_provider.get_response.return_value = direct_response

    response = coding_agent.run_interaction(user_prompt)

    # Verify that tool execution was not attempted
    mock_tool_manager.execute_tool.assert_not_called()

    # Verify that a direct response was generated
    mock_llm_provider.get_response.assert_called_once()

    # Verify the final response
    assert response == direct_response

    # Verify conversation history
    assert len(coding_agent.conversation_history) == 2


def test_agent_handles_tool_execution_error(coding_agent, mock_llm_provider, mock_tool_manager):
    """Test how the agent handles an error during tool execution."""
    user_prompt = "Use a broken tool"
    tool_call = {"tool_name": "broken_tool", "arguments": {}}
    error_message = "Tool 'broken_tool' not found."

    mock_llm_provider.get_tool_usage.return_value = tool_call
    mock_tool_manager.execute_tool.side_effect = ValueError(error_message)

    response = coding_agent.run_interaction(user_prompt)

    # Verify that the error message is returned as the response
    assert f"Error executing tool: {error_message}" in response

    # Verify conversation history includes the error
    assert coding_agent.conversation_history[1]["content"] == f"Error executing tool: {error_message}"

