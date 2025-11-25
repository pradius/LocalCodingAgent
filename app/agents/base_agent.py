"""
Base class for AI agents in the LocalCodingAgent project.

This module provides the BaseAgent class, which encapsulates common functionality
for interacting with an AI model provider (e.g., OpenAI). It handles API client
initialization, system prompt loading, and executing model requests with robust
error handling and logging.
"""

import logging
import os
from pathlib import Path
from typing import Optional

# Using python-dotenv to manage environment variables for API keys
from dotenv import load_dotenv
from openai import APIConnectionError, APIError, OpenAI, RateLimitError

# Load environment variables from a .env file in the project root
load_dotenv()

# Configure logging for the application
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class BaseAgent:
    """
    A base agent that provides a common interface for interacting with an LLM.

    This class is designed to be subclassed by more specialized agents like
    Developer, Planner, or Reviewer. It initializes the API client, loads a
    system prompt from a specified file, and provides a 'run' method to
    process user prompts.

    Attributes:
        model (str): The name of the language model to use (e.g., 'gpt-4-turbo').
        repo_url (Optional[str]): The URL of the code repository, to be used for context
                                  by specialized agents.
        client (OpenAI): The OpenAI API client instance.
        system_prompt (str): The content of the system prompt loaded from a file.
    """

    def __init__(
        self,
        model: str,
        system_prompt_path: str,
        repo_url: Optional[str] = None
    ):
        """
        Initializes the BaseAgent.

        Args:
            model (str): The identifier of the language model to be used.
            system_prompt_path (str): The file path to the system prompt.
            repo_url (Optional[str]): The URL of the code repository relevant to
                                      the agent's task.

        Raises:
            ValueError: If the OpenAI API key is not found in environment variables.
        """
        self.model = model
        self.repo_url = repo_url
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            logger.error("OPENAI_API_KEY environment variable not found.")
            raise ValueError("OPENAI_API_KEY is required to initialize the agent.")

        self.client = OpenAI(api_key=api_key)
        self.system_prompt = self._load_system_prompt(system_prompt_path)

    def _load_system_prompt(self, file_path: str) -> str:
        """
        Loads the system prompt from a text file.

        Args:
            file_path (str): The path to the file containing the system prompt.

        Returns:
            str: The content of the file. Returns a default prompt if the file
                 is not found or an error occurs.
        """
        try:
            prompt_path = Path(file_path)
            if not prompt_path.is_file():
                raise FileNotFoundError(f"System prompt file not found at: {file_path}")

            with open(prompt_path, 'r', encoding='utf-8') as f:
                return f.read()
        except FileNotFoundError as e:
            logger.error(e)
            # Fallback to a default system prompt for resilience
            return "You are a helpful AI assistant."
        except IOError as e:
            logger.error("Error reading system prompt file %s: %s", file_path, e)
            return "You are a helpful AI assistant."

    def run(self, user_prompt: str) -> Optional[str]:
        """
        Executes a query to the language model with the given user prompt.

        Constructs a message list with the system and user prompts and sends it
        to the configured OpenAI model. Handles common API errors gracefully.

        Args:
            user_prompt (str): The user's input/question for the agent.

        Returns:
            Optional[str]: The text content of the model's response, or None if
                           an error occurred that prevented a response.
        """
        if not user_prompt:
            logger.warning("User prompt is empty. Aborting run.")
            return None

        logger.info("Running agent with model: %s", self.model)
        messages = [
            {"role": "system", "content": self.system_prompt},
            {"role": "user", "content": user_prompt},
        ]

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=0.7,  # Balanced value for creativity and predictability
                max_tokens=2048,
                top_p=1.0,
                frequency_penalty=0.0,
                presence_penalty=0.0
            )
            content = response.choices[0].message.content
            logger.info("Successfully received response from the model.")
            return content.strip() if content else None
        except APIConnectionError as e:
            logger.error("Failed to connect to OpenAI API: %s", e)
        except RateLimitError as e:
            logger.error("OpenAI API request exceeded rate limit: %s", e)
        except APIError as e:
            logger.error("OpenAI API returned an error: %s", e)
        except Exception as e:
            logger.error("An unexpected error occurred: %s", e, exc_info=True)

        return None
