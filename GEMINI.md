# GEMINI.md for gh-bridge Project

## Project Overview

**gh-bridge** is a Python library and CLI tool designed to act as a robust, Pythonic wrapper around the GitHub CLI (`gh`). It is engineered specifically for AI Agents and high-automation environments, addressing challenges in enterprise settings where direct token usage might be restricted due to security policies (e.g., SAML/SSO requirements). 

The library leverages the authenticated GitHub CLI session to provide both AI agents and humans with structured, machine-readable data (TOON/JSON/Markdown) or beautiful visual reports (Rich).

**Key Technologies:**
*   **Language:** Python (3.10+)
*   **CLI Wrapper:** GitHub CLI (`gh`)
*   **CLI Framework:** `Typer`
*   **Package Management:** `uv`
*   **Data Models:** `pydantic` (Strict adherence for all feature outputs)
*   **Formatting:** `python-toon` (Agent-optimized), `Rich` (Human-readable)
*   **Linting/Formatting:** `ruff`
*   **Type Checking:** `mypy`
*   **Testing:** `pytest` (Unit & Integration)

## Building and Running

### Prerequisites
1.  **GitHub CLI (`gh`):** Must be installed and authenticated (`gh auth login`).
2.  **uv:** Must be installed.

### Setup
```bash
git clone https://github.com/MohamedHamed19m/gh-bridge
cd gh-bridge
uv sync --all-extras
```

### Running the Project

*   **CLI Usage:**
    ```bash
    # Agent Mode (Default TOON/JSON)
    uv run gh-bridge scan owner/repo
    
    # Human Mode (Rich Tables)
    uv run gh-bridge scan owner/repo --readable
    ```
*   **Running Tests:**
    *   **Unit Tests:** `uv run pytest tests/unit`
    *   **Integration Tests:** `$env:RUN_INTEGRATION_TESTS='1'; uv run pytest tests/integration`
*   **Pre-commit Hooks:** `uv run pre-commit run --all-files`

## Development Conventions

### Core Principles
*   **Strict Pydantic Usage:** All feature layers MUST return Pydantic models. Raw dictionaries are discouraged.
*   **Dual-Mode CLI:** Every CLI command must support both agent-optimized output (default) and human-readable output (`--readable`).
*   **Compositional Architecture:** High-level features are built by composing low-level command wrappers.
*   **Test-Driven Stability:** Maintain >80% coverage and ensure integration tests pass with live API access.

### Project Structure
- **src/gh_wrapper/cli/**: CLI implementation using Typer and command handlers.
- **src/gh_wrapper/core/**: Base executor, exceptions, and caching logic.
- **src/gh_wrapper/commands/**: Low-level GitHub CLI command wrappers.
- **src/gh_wrapper/models/**: Pydantic data models for all outputs.
- **src/gh_wrapper/features/**: High-level features (Tracer, Analytics, Context).

## Feature Implementation Example: Repo Context

- **Command Layer**: `RepoManager.get_repo_basics()` fetches raw API data.
- **Model Layer**: `RepoContextReport` defines the strict schema.
- **Feature Layer**: `RepoContextAnalyzer` orchestrates and returns the model.
- **CLI Layer**: `handle_scan` uses `.model_dump()` for agents or `Rich` for humans.

### The Design Pattern

| Layer | Responsibility | Output Type |
| :--- | :--- | :--- |
| **Command** | Fetching raw data from GitHub CLI | `Dict` / `List[Dict]` |
| **Feature** | Orchestrating logic and transformation | `Pydantic Model` |
| **CLI (Agent)** | Token-efficient transmission | `TOON` / `Markdown` |
| **CLI (Human)** | Visual presentation and UX | `Rich` Renderables |

## Documentation Reference
Detailed usage examples are moved to:
- **[💻 CLI Guide](docs/cli_usage_example.md)**
- **[🐍 Python API Guide](docs/lib_usage_example.md)**
- **[🎨 Visual Demos](docs/lib_usage_example.md#visual-demos)**
