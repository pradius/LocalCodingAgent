# Local Coding Agent

[![Python Version](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Overview

Local Coding Agent is a Python-based AI agent designed to understand and execute coding-related tasks. It leverages Large Language Models (LLMs) and a predefined set of tools to automate software development workflows, from code generation and modification to analysis and testing.

The agent is built with modularity and extensibility in mind, allowing developers to easily integrate new LLM providers, add custom tools, and tailor the agent's behavior to specific needs.

## Features

- **Modular Architecture**: A clean separation of concerns between the agent's core logic, LLM interactions, and tool management.
- **Extensible Toolset**: Easily add new tools for the agent to use (e.g., file system access, code linting, running tests).
- **Pluggable LLM Providers**: Abstracted LLM interface allows for swapping different language models (e.g., OpenAI, Anthropic, local models) with minimal code changes.
- **Test-Driven Development**: The project is set up with a comprehensive testing suite using `pytest`.
- **Modern Python Packaging**: Uses `pyproject.toml` for dependency management and packaging.

## Project Structure

```
repo-LocalCodingAgent/
├── src/
│   └── local_coding_agent/
│       ├── __init__.py
│       ├── agent/
│       │   ├── __init__.py
│       │   └── agent.py        # Core agent logic
│       ├── llm/
│       │   ├── __init__.py
│       │   └── llm_provider.py # Abstractions for LLM providers
│       ├── tools/
│       │   ├── __init__.py
│       │   └── tool_manager.py # Tool registration and execution
│       └── main.py             # Application entry point
├── tests/
│   ├── __init__.py
│   ├── agent/
│   │   └── test_agent.py
│   └── tools/
│       └── test_tool_manager.py
├── .gitignore
├── pyproject.toml
└── README.md
```

## Getting Started

### Prerequisites

- Python 3.9+
- pip

### Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/your-username/repo-LocalCodingAgent.git
    cd repo-LocalCodingAgent
    ```

2.  **Create and activate a virtual environment:**
    ```bash
    python3 -m venv .venv
    source .venv/bin/activate
    ```

3.  **Install the project in editable mode with development dependencies:**
    ```bash
    pip install -e ".[dev]"
    ```

### Usage

The main entry point of the application is `src/local_coding_agent/main.py`.

To run the agent, you can execute the main module:
```bash
python -m src.local_coding_agent.main
```

You will need to configure your LLM provider and API keys as required.

## Development

### Running Tests

To ensure the integrity of the codebase, run the test suite using `pytest`:

```bash
pytest
```

### Contributing

Contributions are welcome! Please feel free to submit a pull request or open an issue.

## License

This project is licensed under the MIT License. See the [LICENSE](https://opensource.org/licenses/MIT) file for details.
