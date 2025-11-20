"""
Abstract base class for LLM providers.

This module defines the interface for interacting with Large Language Models.
Implementations of this interface can be created for specific LLM providers
(e.g., OpenAI, Anthropic, a local model).
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, List


class LLMProvider(ABC):
    """An abstract base class for LLM providers."""

    @abstractmethod
    def get_response(self, prompt: str, conversation_history: List[Dict[str, str]] = None) -> str:
        """
        Get a response from the LLM.

        Args:
            prompt: The user's prompt.
            conversation_history: A list of previous messages in the conversation.

        Returns:
            The LLM's response as a string.
        """

    @abstractmethod
    def get_tool_usage(self, prompt: str, tools: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Determine which tool the LLM wants to use and with what arguments.

        Args:
            prompt: The user's prompt.
            tools: A list of available tools, formatted for the LLM.

        Returns:
            A dictionary representing the tool call, e.g.,
            {'tool_name': 'file_reader', 'arguments': {'file_path': 'src/main.py'}}
        """
