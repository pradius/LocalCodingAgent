# Local Coding Agent

This project is a sophisticated AI-powered coding agent designed to understand and execute software development tasks. It leverages a modular architecture with different agent roles (Planner, Developer, Reviewer) and can be configured to use either commercial LLMs (like OpenAI's GPT series) or a local LLM via Ollama.

## Table of Contents

- [Features](#features)
- [Project Structure](#project-structure)
- [Setup and Installation](#setup-and-installation)
- [Configuration](#configuration)
  - [Using OpenAI](#using-openai)
  - [Using a Local LLM with Ollama](#using-a-local-llm-with-ollama)
- [Usage](#usage)
- [Running Tests](#running-tests)

## Features

- **Modular Agent-based Architecture**: Specialized agents for planning, development, and code review.
- **Tool Integration**: Agents can use tools (e.g., file system access, command execution).
- **Flexible LLM Backend**: Easily switch between OpenAI's API and a local Ollama instance.
- **State Management**: Keeps track of the task progress and history.
- **Clear Prompt Engineering**: Structured prompts for reliable and consistent outputs.

## Project Structure

```
repo-LocalCodingAgent/
├── app/                  # Main application logic
│   ├── agents/           # Agent implementations
│   └── main.py           # Entry point for the application
├── config.yaml           # Configuration file for the agent
├── docs/                 # Project documentation
├── prompts/              # System and user prompts for agents
├── pyproject.toml        # Project metadata and dependencies
├── README.md             # This file
├── requirements.txt      # Python package dependencies
├── scripts/              # Helper scripts
├── setup.py              # Setup script for packaging
├── src/                  # Source code for the core agent framework
│   ├── agents/           # Base agent class and role definitions
│   ├── tools/            # Available tools for agents
│   └── utils/            # Utility functions
└── tests/                # Unit and integration tests
```

## Setup and Installation

1.  **Clone the repository:**
    ```bash
    git clone <repository-url>
    cd repo-LocalCodingAgent
    ```

2.  **Create a virtual environment:**
    ```bash
    python3 -m venv .venv
    source .venv/bin/activate
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **(Optional) Install Ollama:**
    If you want to use a local LLM, you need to install and run [Ollama](https://ollama.com/). After installation, pull the model you want to use, for example:
    ```bash
    ollama pull llama3
    ```

## Configuration

The agent's behavior is controlled by the `config.yaml` file.

### Using OpenAI

To use an OpenAI model, set up your configuration as follows:

```yaml
llm:
  provider: "openai" # or "anthropic", "google"
  model: "gpt-4-turbo"
  temperature: 0.1
  # Make sure your OPENAI_API_KEY is set as an environment variable

# ... other configurations
```

### Using a Local LLM with Ollama

To use a local model served by Ollama, modify your `config.yaml`:

```yaml
llm:
  provider: "local" # Use the 'local' provider
  model: "llama3"    # The name of the model you pulled with Ollama
  temperature: 0.1
  api_base: "http://localhost:11434/v1" # Ollama's OpenAI-compatible API endpoint
  api_key: "ollama" # Required by the client, can be any non-empty string

# ... other configurations
```
The `api_base` and `api_key` fields are crucial for connecting to the local server.

## Usage

Run the agent from the main directory:

```bash
python main.py --task "Implement a feature that does X, Y, and Z."
```

The agent will read the `config.yaml`, initialize the appropriate LLM, and start working on the task.

## Running Tests

To run the test suite:

```bash
pytest
```
