# Technology Stack

## Core Stack
- **Programming Language:** Python 3.10+ (Tested on 3.13)
- **Package Manager:** `uv`
- **CLI Execution:** GitHub CLI (`gh`) wrapped via `subprocess` and `json` (handled by `GHExecutor`).
- **Data Handling:** `pydantic` for data validation, standard library (`json`, `dataclasses`).
- **UI & Formatting:** `rich` for enhanced terminal output and logging.
- **CLI Framework:** `Click` (Currently used), `Typer` (Planned for full user-facing CLI interface).

## Development & Tooling
- **Testing:** `pytest` (including `pytest-cov`, `pytest-mock`). Integration tests require a real `gh` CLI and `GH_TOKEN`.
- **Linting & Formatting:** `ruff`
- **Type Checking:** `mypy`
- **Build System:** `hatchling`
- **CI/CD:** GitHub Actions

## Future Enhancements
- **Async Support:** Explore `httpx` for direct API calls to complement `gh` CLI where performance is critical.
