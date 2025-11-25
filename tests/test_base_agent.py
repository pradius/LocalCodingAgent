"""
Unit tests for the BaseAgent class.

This test suite uses pytest and pytest-mock to test the functionality of BaseAgent
without making actual API calls to OpenAI. It covers initialization, system prompt
loading, and the 'run' method's success and failure scenarios.
"""
import sys
from pathlib import Path
import pytest
from unittest.mock import MagicMock, patch

# Add the project root to the Python path to allow importing from 'app'
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.agents.base_agent import BaseAgent
from openai import APIConnectionError, RateLimitError, APIError


@pytest.fixture(scope="function")
def mock_env_vars(monkeypatch):
    """Fixture to set mock environment variables for the duration of a test."""
    monkeypatch.setenv("OPENAI_API_KEY", "test-api-key")

@pytest.fixture
def mock_openai_client():
    """Fixture to create a mock OpenAI client and patch it into the agent module."""
    with patch('app.agents.base_agent.OpenAI') as mock_openai:
        mock_instance = MagicMock()
        mock_openai.return_value = mock_instance
        yield mock_instance

@pytest.fixture
def temp_prompt_file(tmp_path):
    """Fixture to create a temporary system prompt file for testing."""
    prompt_content = "You are a test assistant."
    file_path = tmp_path / "system_prompt.txt"
    file_path.write_text(prompt_content, encoding='utf-8')
    return file_path, prompt_content

def test_initialization_success(mock_env_vars, temp_prompt_file, mock_openai_client):
    """
    Tests successful initialization of the BaseAgent.
    Verifies that all attributes are set correctly and the API client is instantiated.
    """
    prompt_path, prompt_content = temp_prompt_file
    agent = BaseAgent(
        model="gpt-test",
        system_prompt_path=str(prompt_path),
        repo_url="https://github.com/test/repo"
    )
    assert agent.model == "gpt-test"
    assert agent.repo_url == "https://github.com/test/repo"
    assert agent.system_prompt == prompt_content
    # Ensure the client was created with the correct key
    from app.agents.base_agent import OpenAI
    OpenAI.assert_called_once_with(api_key="test-api-key")

def test_initialization_no_api_key(monkeypatch):
    """
    Tests that BaseAgent raises ValueError if OPENAI_API_KEY is not set.
    """
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    with pytest.raises(ValueError, match="OPENAI_API_KEY is required"):
        BaseAgent(model="gpt-test", system_prompt_path="dummy.txt")

def test_load_system_prompt_file_not_found(mock_env_vars, caplog):
    """
    Tests fallback behavior when the system prompt file is not found.
    The agent should log an error and use a default prompt.
    """
    agent = BaseAgent(model="gpt-test", system_prompt_path="non_existent_file.txt")
    assert "System prompt file not found" in caplog.text
    assert agent.system_prompt == "You are a helpful AI assistant."

def test_run_success(mock_env_vars, mock_openai_client, temp_prompt_file):
    """
    Tests a successful 'run' of the agent, mocking the API response.
    Verifies that the response content is correctly extracted and stripped.
    """
    # Arrange
    prompt_path, _ = temp_prompt_file
    agent = BaseAgent(model="gpt-test", system_prompt_path=str(prompt_path))

    mock_response = MagicMock()
    mock_response.choices[0].message.content = "  This is a test response.  "
    mock_openai_client.chat.completions.create.return_value = mock_response

    user_prompt = "Hello, world!"

    # Act
    result = agent.run(user_prompt)

    # Assert
    assert result == "This is a test response."
    mock_openai_client.chat.completions.create.assert_called_once()
    call_args, _ = mock_openai_client.chat.completions.create.call_args
    assert call_args[0]['model'] == "gpt-test"
    assert call_args[0]['messages'][-1]['role'] == 'user'
    assert call_args[0]['messages'][-1]['content'] == user_prompt

def test_run_empty_user_prompt(mock_env_vars, mock_openai_client, temp_prompt_file, caplog):
    """
    Tests that the agent handles an empty user prompt gracefully.
    """
    prompt_path, _ = temp_prompt_file
    agent = BaseAgent(model="gpt-test", system_prompt_path=str(prompt_path))

    result = agent.run("")

    assert result is None
    assert "User prompt is empty" in caplog.text
    mock_openai_client.chat.completions.create.assert_not_called()

@pytest.mark.parametrize("error_class", [
    APIConnectionError(request=MagicMock()),
    RateLimitError(request=MagicMock(), response=MagicMock(), body=None),
    APIError(request=MagicMock(), message="API Error", body=None, code=500),
    Exception("A generic error occurred")
])
def test_run_api_errors(mock_env_vars, mock_openai_client, temp_prompt_file, caplog, error_class):
    """
    Tests that various API and generic errors are caught, logged, and return None.
    """
    # Arrange
    prompt_path, _ = temp_prompt_file
    agent = BaseAgent(model="gpt-test", system_prompt_path=str(prompt_path))
    mock_openai_client.chat.completions.create.side_effect = error_class

    # Act
    result = agent.run("A prompt that will fail.")

    # Assert
    assert result is None
    assert "ERROR" in caplog.text # Check that an error was logged
    if isinstance(error_class, Exception):
        assert str(error_class) in caplog.text

