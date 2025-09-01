# Gemini AI Coding Agent

## Description

This project implements a command-line AI coding agent powered by the Google Gemini API. The agent can understand and execute tasks related to file manipulation and code execution within a specified workspace. It's designed to be a "careful" agent, meaning it prefers to understand its environment (by listing and reading files) before taking actions like writing or executing code.

## Features

-   **Interactive Command-Line Interface:**  Interact with the agent directly from your terminal.
-   **File System Operations:**
    -   List files and directories.
    -   Read the contents of any file.
    -   Write or overwrite files.
-   **Code Execution:** Run Python scripts.
-   **Extensible Toolset:** The agent's capabilities are defined by a set of "tools" (functions) that can be expanded.
-   **Example Tool:** Includes a sample `calculator` application that the agent can be instructed to use.

## Getting Started

### Prerequisites

-   Python 3.x
-   An API key for the Google Gemini API.

### Installation

1.  **Clone the repository:**
    ```bash
    git clone <repository-url>
    cd <repository-directory>/aiagent
    ```

2.  **Install dependencies:**
    This project uses `uv` for package management.
    ```bash
    pip install uv
    uv pip install -r requirements.txt 
    ```
    *(Note: You'll need to create a `requirements.txt` from `pyproject.toml` or install manually)*

3.  **Set up your environment variables:**
    Create a `.env` file in the `aiagent` directory and add your Gemini API key:
    ```
    GEMINI_API_KEY="your_api_key_here"
    ```

## Usage

Run the agent from the command line, providing a prompt for the task you want it to perform.

```bash
python main.py "Your task description here"
```

### Examples

-   **List files in the current directory:**
    ```bash
    python main.py "list all the files in the current directory"
    ```

-   **Read a file:**
    ```bash
    python main.py "read the contents of the file named main.py"
    ```

-   **Use the calculator:**
    ```bash
    python main.py "use the calculator to evaluate '10 + 5 * 2'"
    ```
- **Verbose mode**
    ```bash
    python main.py "use the calculator to evaluate '10 + 5 * 2'" --verbose
    ```

## Project Structure

```
aiagent/
├── .venv/
├── calculator/           # Example tool: a command-line calculator
│   ├── main.py
│   ├── pkg/
│   └── tests.py
├── functions/            # Core functions (tools) for the agent
│   ├── call_function.py
│   ├── get_file_content.py
│   ├── get_files_info.py
│   ├── run_python.py
│   └── write_file.py
├── .gitignore
├── main.py               # Main entry point for the AI agent
├── pyproject.toml
├── README.md
├── tests.py
└── uv.lock
```

```
