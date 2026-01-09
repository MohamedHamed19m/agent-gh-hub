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

## Development Conventions

### Core Principles
*   **Test-Driven Development (TDD):** Tests should ideally be written before implementation.
*   **High Code Coverage:** Maintain >80% code coverage for unit tests.
*   **Clean Commits:** Adhere to Conventional Commits format (e.g., `feat(scope): description`).
*   **Compositional Architecture:** High-level features are built by composing low-level command wrappers.

### Style and Formatting
*   **Line Length:** Maximum 88 characters.
*   **Indentation:** 4 spaces per level.
*   **Docstrings:** Use `"""triple double quotes"""` for all public modules, functions, classes, and methods.
*   **Type Annotations:** Strongly encouraged for all public APIs.

### Testing Strategy
*   **Unit Tests:** Mock external dependencies (like `gh` CLI calls) to verify logic in isolation.
*   **Integration Tests:** Interact with the actual GitHub CLI/API to test end-to-end functionality.

### Feature Design Philosophy
*   **Compositional Architecture:** New features should leverage existing low-level command wrappers.
*   **AI-Native Output:** Prioritize structured, machine-readable (JSON) output optimized for AI agents.

## Project Structure

- **src/gh_wrapper/core/**: Base executor, exceptions, and caching logic.
- **src/gh_wrapper/commands/**: Low-level GitHub CLI command wrappers.
- **src/gh_wrapper/models/**: Pydantic data models for structured API responses.
- **src/gh_wrapper/features/**: High-level features that compose commands and models into insights.
- **src/gh_wrapper/utils/**: Helper utilities.

## Feature Implementation Example: Repo Analysis

- **Command Layer**: `CommitsManager.list_commits()` fetches raw API data.
- **Model Layer**: `BranchStats` defines the structured output schema.
- **Feature Layer**: `BranchAnalyzer` orchestrates the analysis logic (health score, contributors).

### Usage Example

```python
from gh_wrapper.features.branch_analytics import BranchAnalyzer

analyzer = BranchAnalyzer(executor)
stats = analyzer.analyze_branch("main")
print(stats.health_score)
```

## Feature Implementation Example: Feature Tracer

- **Command Layer**: `FileManager.search_in_files()`, `CommitsManager.list_commits()`, `PRManager.list_prs()`.
- **Model Layer**: `MultiRepoFeatureTrace` and `FeatureTrace` define the aggregated result schema.
- **Feature Layer**: `FeatureTracer` orchestrates cross-repo searching and ranking.

### Usage Example

```python
from gh_wrapper.features.feature_tracer import FeatureTracer

tracer = FeatureTracer(executor)
report = tracer.trace_code("auth", branches=["main", "develop"])
```

## Feature Implementation Example: PR Review

- **Command Layer**: `PRManager.get_pr_diff()` fetches raw diff data.
- **Model Layer**: `PrReviewOutput` defines the structured output schema.
- **Feature Layer**: `PrReviewAnalyzer` parses diffs and generates summaries.

### Usage Example

```python
from gh_wrapper.features.pr_review_analyzer import PrReviewAnalyzer

analyzer = PrReviewAnalyzer(pr_manager)
report = analyzer.analyze_pr(pr_input)
print(analyzer.format_as_markdown(report))
```


### The Design Pattern

For your `repo_analysis` feature, here is how you should distribute the logic:

| Layer | Responsibility | Example Logic |
| :--- | :--- | :--- |
| **Command** | Fetching raw data from GitHub | `list_branches()`, `get_commit_history()` |
| **Feature** | Orchestrating and Logic | Loop through branches ðŸ”„, compare dates ðŸ“…, calculate "staleness" score âš–ï¸ |


- The Golden Rule
RepoManager (Command Layer): "I fetch raw data from GitHub API"
RepoAnalyzer (Feature Layer): "I transform that data into insights"