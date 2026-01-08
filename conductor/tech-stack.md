# Technology Stack

## Core Stack
- **Programming Language:** Python 3.10+
- **Package Manager:** `uv`
- **CLI Execution:** GitHub CLI (`gh`) wrapped via `subprocess` and `json` (handled by `GHExecutor`).
- **Data Handling:** Standard library (`json`, `dataclasses`).
- **CLI Framework:** `Typer` (Planned for full user-facing CLI interface).

## Development & Tooling
- **Testing:** `pytest` (including `pytest-cov`, `pytest-mock`). Integration tests require a real `gh` CLI and `GH_TOKEN`.
- **Linting & Formatting:** `ruff`
- **Type Checking:** `mypy`
- **Build System:** `hatchling`
- **CI/CD:** GitHub Actions

## Future Enhancements
- **Terminal Formatting:** `rich` for enhanced terminal output.
- **Validation:** `pydantic` for configuration and data validation.
