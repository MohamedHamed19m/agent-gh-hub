# GEMINI.md for gh-bridge Project

## Project Overview

**gh-bridge** is a Python library designed to act as a robust, Pythonic wrapper around the GitHub CLI (`gh`). It is engineered specifically for AI Agents and high-automation environments, addressing challenges in enterprise settings where direct token usage might be restricted due to security policies (e.g., SAML/SSO requirements). The library leverages the authenticated GitHub CLI session to provide AI agents with structured, JSON-formatted data from GitHub repositories, enhancing their capabilities for tasks like code analysis, repository exploration, and workflow automation.

**Key Technologies:**
*   **Language:** Python (3.10+)
*   **CLI Wrapper:** GitHub CLI (`gh`)
*   **Package Management:** `uv`
*   **Data Models:** `pydantic` (for structured data and validation)
*   **Data Handling:** standard library (`json`, `dataclasses`)
*   **Linting/Formatting:** `ruff`
*   **Type Checking:** `mypy`
*   **Testing:** `pytest`
*   **Build System:** `hatchling`
*   **CI/CD:** GitHub Actions

## Building and Running

### Prerequisites
1.  **GitHub CLI (`gh`):** Must be installed and authenticated (`gh auth login`). Use `gh auth status` to verify. The library automatically uses the host and account from your active CLI session; manual `GH_HOST` configuration is not required for standard usage.
2.  **uv:** Must be installed.

### Setup
```bash
# Clone the repository
git clone https://github.com/MohamedHamed19m/gh-bridge
cd gh-bridge

# Install and sync dependencies using uv
uv sync --all-extras
```

### Running the Project

*   **Running Tests:**
    *   **Unit Tests:** `uv run pytest tests/unit --cov=src/gh_wrapper` (Aim for >80% coverage)
    *   **Integration Tests:** `uv run pytest tests/integration` (Requires `GH_TOKEN` or equivalent authentication)
*   **Running the Demo Script:**
    ```bash
    python scripts/demo_usage.py
    ```
*   **Type Checking:**
    ```bash
    uv run mypy .
    ```
*   **Linting and Formatting:**
    ```bash
    uv run ruff check .
    uv run ruff format .
    ```
*   **Pre-commit Hooks:**
    ```bash
    uv run pre-commit install
    ```

**Note:** The `scripts/setup_dev.sh` script can be used for initial setup:
```bash
# Run this script to install uv, sync dependencies, and setup pre-commit hooks
bash scripts/setup_dev.sh
```

## Development Conventions

### Core Principles
*   **Test-Driven Development (TDD):** Tests should ideally be written before implementation.
*   **High Code Coverage:** Maintain >80% code coverage for unit tests.
*   **Clean Commits:** Adhere to Conventional Commits format (e.g., `feat(scope): description`).
*   **Compositional Architecture:** High-level features are built by composing low-level command wrappers.

### Style and Formatting
*   **Line Length:** Maximum 88 characters.
*   **Indentation:** 4 spaces per level.
*   **Docstrings:** Use `"""triple double quotes"""` for all public modules, functions, classes, and methods, including `Args:`, `Returns:`, and `Raises:` sections where applicable.
*   **Type Annotations:** Strongly encouraged for all public APIs, enforced by `mypy` with `disallow_untyped_defs = true`.
*   **Naming:** `snake_case` for modules, functions, variables; `PascalCase` for classes; `ALL_CAPS_WITH_UNDERSCORES` for constants.
*   **Imports:** Grouped and ordered: standard library, third-party, own application imports.

### Testing Strategy
*   **Unit Tests:** Mock external dependencies (like `gh` CLI calls) to verify logic in isolation.
*   **Integration Tests:** Interact with the actual GitHub CLI/API to test end-to-end functionality. These require authentication and are not included in coverage stats.

### Contribution Guidelines
*   Ensure all Pull Requests pass `ruff` linting and `mypy` type checks.
*   Follow the established development workflow and testing strategies.
*   Refer to `conductor/code_styleguides/` for detailed style guidelines.

### Feature Design Philosophy
*   **Compositional Architecture:** New features should leverage existing low-level command wrappers.
*   **AI-Native Output:** Prioritize structured, machine-readable (JSON) output optimized for AI agents.
*   **Performance:** Minimize latency; use caching where appropriate.

### Error Handling
*   Standardized error envelopes with `error` field, status code, and actionable messages.
*   `GHCommandError` and `GHNotInstalledError` are used for specific CLI-related issues.


### ðŸ›ï¸ The Design Pattern

For your `repo_analysis` feature, here is how you should distribute the logic:

| Layer | Responsibility | Example Logic |
| :--- | :--- | :--- |
| **Command** | Fetching raw data from GitHub | `list_branches()`, `get_commit_history()` |
| **Feature** | Orchestrating and Logic | Loop through branches ðŸ”„, compare dates ðŸ“…, calculate "staleness" score âš–ï¸ |


ðŸŽ¯ The Golden Rule
RepoManager (Command Layer): "I fetch raw data from GitHub API"
RepoAnalyzer (Feature Layer): "I transform that data into insights"

## Project Structure

- **src/gh_wrapper/core/**: Base executor, exceptions, and caching logic.
- **src/gh_wrapper/commands/**: Low-level GitHub CLI command wrappers (e.g., repository, commits, files).
- **src/gh_wrapper/models/**: Pydantic data models for structured API responses.
- **src/gh_wrapper/features/**: High-level features that compose commands and models into insights.
- **src/gh_wrapper/utils/**: Helper utilities.

## Feature Implementation Example: Repo Analysis

- **Command Layer**: `CommitsManager.get_commits_for_analysis()` fetches raw API data.
- **Model Layer**: `CommitAnalysisReport` defines the structured output schema.
- **Feature Layer**: `RepoAnalyzer` orchestrates the analysis logic (daily trends, contributor activity, time patterns).

### Usage Example

```python
from gh_wrapper.features.repo_analysis import RepoAnalyzer

analyzer = RepoAnalyzer(commits_manager)
report = analyzer.analyze_commit_patterns(branches=["main"], days_back=30)
print(analyzer.format_as_markdown(report))
```
## Feature Implementation Example: Feature Tracer

- **Command Layer**: FileManager.search_in_files(), CommitsManager.get_commits_for_analysis(), PRManager.list_prs() fetch raw data.
- **Model Layer**: MultiRepoFeatureTrace and FeatureTrace define the aggregated result schema.
- **Feature Layer**: FeatureTracer orchestrates cross-repo searching, client-side filtering, and contributor ranking.

### Usage Example

`python
from gh_wrapper.features.feature_tracer import FeatureTracer

tracer = FeatureTracer()
report = tracer.trace_feature(keyword=\
secure
boot\, repos=[\org/repo1\, \org/repo2\])
print(tracer.format_as_markdown(report))
``
