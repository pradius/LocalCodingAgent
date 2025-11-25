"""
This module contains the core logic of the AI coding agent.
"""

from typing import Any, Dict, List

from local_coding_agent.llm.llm_provider import LLMProvider
from local_coding_agent.tools.tool_manager import ToolManager


class CodingAgent:
    """
    The main agent class that orchestrates the workflow.
    """

    def __init__(self, llm_provider: LLMProvider, tool_manager: ToolManager):
        """
        Initialize the CodingAgent.

        Args:
            llm_provider: An instance of a class that implements LLMProvider.
            tool_manager: An instance of ToolManager with registered tools.
        """
        self.llm_provider = llm_provider
        self.tool_manager = tool_manager
        self.conversation_history: List[Dict[str, str]] = []

    def run_interaction(self, user_prompt: str) -> str:
        """
        Run a single interaction with the user.

        This method takes a user prompt, decides whether to use a tool or
        generate a direct response, and returns the result.

        Args:
            user_prompt: The user's input.

        Returns:
            The agent's response, which could be the result of a tool or a
            direct text response from the LLM.
        """
        self.conversation_history.append({"role": "user", "content": user_prompt})

        # 1. Decide if a tool is needed
        tool_schemas = self.tool_manager.get_tool_schemas()
        tool_call = self.llm_provider.get_tool_usage(user_prompt, tool_schemas)

        if tool_call:
            # 2. Execute the tool
            tool_name = tool_call.get("tool_name")
            arguments = tool_call.get("arguments", {})
            try:
                tool_result = self.tool_manager.execute_tool(tool_name, **arguments)
                response_content = str(tool_result)
            except ValueError as e:
                response_content = f"Error executing tool: {e}"

            self.conversation_history.append({"role": "assistant", "content": response_content})
        else:
            # 3. Generate a direct response
            response_content = self.llm_provider.get_response(user_prompt, self.conversation_history)
            self.conversation_history.append({"role": "assistant", "content": response_content})

        return response_content
