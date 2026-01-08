# Development Workflow

## Overview
This workflow is designed for the `gh-wrapper` library, prioritizing robust testing, high code coverage, and a clean release process suitable for a Python package.

## Core Principles
1.  **Test-Driven Development (TDD):** Write tests before implementation whenever possible.
2.  **High Coverage:** Maintain >80% code coverage for unit tests.
3.  **Clean Commits:** Use Conventional Commits. Task summaries go directly into commit messages.
4.  **Integration vs. Unit:** Clearly separate unit tests (mocked) from integration tests (real API).

## Testing Strategy

### Unit Tests
-   **Goal:** Verify logic in isolation.
-   **Requirement:** >80% coverage.
-   **Command:** `uv run pytest tests/unit --cov=src/gh_wrapper`
-   **Mocking:** Use `pytest-mock` to mock all external `gh` CLI calls.

### Integration Tests
-   **Goal:** Verify interaction with the real GitHub CLI/API.
-   **Requirement:** Best effort. Excluded from coverage stats.
-   **Prerequisite:** Requires a valid `GH_TOKEN`.
-   **Command:** `uv run pytest tests/integration` (or set `RUN_INTEGRATION_TESTS=1`)

## Daily Development Loop
1.  **Pick a Task:** Select a task from the current Phase in `plan.md`.
2.  **Implement:**
    -   Write unit tests first.
    -   Implement the feature/fix.
    -   Verify with `uv run pytest`.
3.  **Commit:**
    -   Stage changes.
    -   Commit with a clear summary: `feat(scope): detailed description of change`
    -   *Note: No Git Notes required.*

## Phase Completion Protocol
When a Phase in `plan.md` is complete:
1.  **Run All Tests:** Execute the full suite (unit + integration).
2.  **Verify Coverage:** Ensure unit test coverage is >80%.
3.  **Create Checkpoint:**
    -   Commit with message: `conductor(checkpoint): Phase X complete`
4.  **Update Plan:** specific the commit SHA in `plan.md` for the completed phase.

## Release Workflow

### Pre-1.0 (Unstable) Releases
-   **Versioning:** `v0.x.x` (Unstable API).
-   **Target:** GitHub Releases (Primary), TestPyPI (Optional).

### Pre-Release Checklist
- [ ] All tests passing.
- [ ] Coverage >80% for unit tests.
- [ ] No type errors (`mypy`).
- [ ] No linting errors (`ruff`).
- [ ] README examples tested.
- [ ] CHANGELOG.md updated.

### Release Steps
1.  **Update Version:** Bump version in `pyproject.toml`.
2.  **Verify:** Run `uv run pytest` and ensure clean lint/types.
3.  **Build:** Run `uv build`.
4.  **Publish (Test):** `uv publish --repository testpypi` (Optional).
5.  **Tag & Release:**
    -   Create a GitHub Release tagged `v0.x.x`.
    -   Generate notes from `git log`.
    -   Mark as "Pre-release".

### Post-1.0 (Stable) Releases
-   Follow strict Semantic Versioning.
-   Publish to production PyPI.
-   Document breaking changes extensively.