# Local Coding Agent

This project provides a framework for creating specialized AI agents for coding tasks. It includes a `BaseAgent` that handles the core logic of interacting with a Large Language Model (LLM) like OpenAI's GPT series.

## Project Structure

```
repo-LocalCodingAgent/
├── app/
│   ├── __init__.py
│   └── agents/
│       ├── __init__.py
│       └── base_agent.py   # Core agent logic
├── prompts/
│   └── system_prompt_template.md # Example system prompt
├── tests/
│   ├── __init__.py
│   └── test_base_agent.py # Unit tests for the BaseAgent
├── .env.example            # Example environment variables file
├── .gitignore
├── README.md
└── requirements.txt        # Project dependencies
```

## Setup and Installation

1.  **Clone the repository:**
    ```bash
    git clone <your-repo-url>
    cd repo-LocalCodingAgent
    ```

2.  **Create a virtual environment:**
    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Set up environment variables:**
    -   Copy the example `.env` file:
        ```bash
        cp .env.example .env
        ```
    -   Edit the `.env` file and add your OpenAI API key:
        ```
        OPENAI_API_KEY="your_openai_api_key_here"
        ```

## Running Tests

To ensure the `BaseAgent` is working correctly, run the unit tests using `pytest`:

```bash
pytest
```

## Basic Usage

The `BaseAgent` is designed to be imported and used by other, more specific agents. Here's a simple example of how you might use it directly:

```python
from app.agents.base_agent import BaseAgent

# Initialize the agent
# Make sure 'prompts/system_prompt_template.md' exists
agent = BaseAgent(
    model="gpt-4-turbo",
    system_prompt_path="prompts/system_prompt_template.md",
    repo_url="https://github.com/example/my-project"
)

# Run the agent with a user prompt
user_prompt = "Explain the concept of recursion in Python with a simple code example."
response = agent.run(user_prompt)

if response:
    print("AI Response:")
    print(response)
else:
    print("Failed to get a response from the agent.")

```
