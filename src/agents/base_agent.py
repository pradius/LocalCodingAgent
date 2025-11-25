"""
Base Agent Module

This module defines the foundational `BaseAgent` class, which serves as the
template for all other specialized agents within the system (e.g., Planner,
Developer, Reviewer). It handles the core logic for interacting with a
Language Learning Model (LLM), managing state, and processing tasks.

The key feature of this module is its ability to abstract the LLM provider,
allowing for seamless switching between commercial APIs (like OpenAI) and
local models served through platforms like Ollama. This flexibility is
achieved by dynamically configuring the LLM client based on the `config.yaml`
file.

Classes:
    BaseAgent: An abstract base class for creating AI agents.

Key Responsibilities:
-   Loading and validating agent configuration.
-   Initializing the appropriate LLM client (e.g., OpenAI or a local client).
-   Maintaining conversation history and state.
-   Providing a standardized interface (`run` method) for agent execution.
-   Logging and error handling.
"""

import os
import logging
from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional

from openai import OpenAI, OpenAIError

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class BaseAgent(ABC):
    """
    An abstract base class for creating AI agents.

    This class provides the core structure for an agent, including initialization
    of the language model client, state management, and a common interface for
    execution. It is designed to be subclassed by specific agent types that
    implement their own `run` logic.

    Attributes:
        llm_config (Dict[str, Any]): Configuration for the language model.
        client (OpenAI): The client instance for interacting with the LLM.
        system_prompt (str): The system prompt that defines the agent's role.
        history (List[Dict[str, str]]): A list to store the conversation history.
    """

    def __init__(self, config: Dict[str, Any], system_prompt: str):
        """
        Initializes the BaseAgent with configuration and a system prompt.

        It sets up the LLM client based on the specified provider (e.g., 'openai'
        or 'local'). If the provider is 'local', it expects an Ollama-compatible
        API endpoint.

        Args:
            config (Dict[str, Any]): The agent's configuration, typically loaded
                                     from a YAML file. Must contain an 'llm' key.
            system_prompt (str): The system prompt to guide the agent's behavior.

        Raises:
            ValueError: If the 'llm' configuration is missing or invalid.
            ConnectionError: If the client fails to connect to the LLM service.
        """
        if 'llm' not in config:
            raise ValueError("LLM configuration is missing in the provided config.")

        self.llm_config: Dict[str, Any] = config['llm']
        self.system_prompt: str = system_prompt
        self.history: List[Dict[str, str]] = []
        self.client: OpenAI = self._init_client()

    def _init_client(self) -> OpenAI:
        """
        Initializes the LLM client based on the configuration.

        Supports 'openai' and 'local' providers. For 'local', it configures the
        client to connect to a local OpenAI-compatible API server like Ollama.

        Returns:
            OpenAI: An instance of the OpenAI client configured for the
                    specified provider.

        Raises:
            ValueError: If the provider is not supported or if required
                        configuration for a provider is missing.
            ConnectionError: If the client cannot be initialized, potentially
                             due to authentication or network issues.
        """
        provider = self.llm_config.get("provider", "openai").lower()
        logger.info(f"Initializing LLM client for provider: {provider}")

        try:
            if provider == "local":
                # Configuration for local LLM (e.g., via Ollama)
                api_base = self.llm_config.get("api_base")
                if not api_base:
                    raise ValueError("Missing 'api_base' for local LLM provider.")

                return OpenAI(
                    base_url=api_base,
                    api_key=self.llm_config.get("api_key", "ollama") # Default key for Ollama
                )
            elif provider == "openai":
                # Standard OpenAI configuration
                api_key = os.getenv("OPENAI_API_KEY")
                if not api_key:
                    raise ValueError("OPENAI_API_KEY environment variable not set.")
                return OpenAI(api_key=api_key)
            else:
                # Extendable to other providers like Anthropic, Google, etc.
                raise ValueError(f"Unsupported LLM provider: {provider}")

        except Exception as e:
            logger.error(f"Failed to initialize LLM client for provider '{provider}': {e}")
            raise ConnectionError(f"Could not connect to LLM provider '{provider}'. Please check your configuration and network.") from e

    def _chat_completion(self, messages: List[Dict[str, str]]) -> Optional[str]:
        """
        Sends a request to the LLM and gets a response.

        Args:
            messages (List[Dict[str, str]]): The list of messages forming the
                                             conversation context.

        Returns:
            Optional[str]: The content of the assistant's response, or None if
                           an error occurred.
        """
        try:
            response = self.client.chat.completions.create(
                model=self.llm_config.get("model", "gpt-4-turbo"),
                messages=messages,
                temperature=self.llm_config.get("temperature", 0.1),
                max_tokens=self.llm_config.get("max_tokens", 4096),
            )
            content = response.choices[0].message.content
            if content is None:
                logger.warning("Received a null response from the LLM.")
                return None
            return content.strip()
        except OpenAIError as e:
            logger.error(f"An API error occurred: {e}")
            return None
        except Exception as e:
            logger.error(f"An unexpected error occurred during chat completion: {e}")
            return None

    @abstractmethod
    def run(self, **kwargs) -> Any:
        """
        The main execution method for the agent.

        This method must be implemented by subclasses to define the agent's
        specific workflow and logic.
        """
        pass

    def get_history(self) -> List[Dict[str, str]]:
        """
        Returns the conversation history.

        Returns:
            List[Dict[str, str]]: The list of messages exchanged with the LLM.
        """
        return self.history

    def clear_history(self) -> None:
        """Resets the conversation history."""
        logger.info("Clearing conversation history.")
        self.history = []

