# Implementation Plan: pr_review Feature

## 1. Overview
This plan details the development steps for the `pr_review` feature, as defined in `spec.md`. It follows the TDD principles and testing strategies outlined in `workflow.md`. The work is divided into phases to facilitate a structured approach.

## 2. Phases and Tasks

### Phase 1: Command Layer Development (Agent A) - PR Data Fetching

**Objective:** Implement low-level command wrappers to fetch comprehensive Pull Request data required for the `pr_review` feature.

*   **Task: Define and Implement `PRManager` Extensions**
    *   [ ] Sub-task: Create or extend `PRManager` to fetch PR details including files, diffs, and basic status.
        *   Files: `src/gh_wrapper/commands/pull_requests.py`
    *   [ ] Sub-task: Implement functionality to retrieve `gh pr view --json` data.
    *   [ ] Sub-task: Implement functionality to retrieve `gh pr diff <PR_ID> --patch` or `--diff` data, which provides raw diffs essential for analysis.
    *   [ ] Sub-task: Implement functionality to retrieve branch comparison data if a target branch is specified.
        *   Files: `src/gh_wrapper/commands/pull_requests.py`
*   **Task: Write Unit Tests for `PRManager` Extensions**
    *   [ ] Sub-task: Create `test_pull_requests.py` if it doesn't exist, or extend existing test file.
        *   Files: `tests/unit/commands/test_pull_requests.py`
    *   [ ] Sub-task: Write unit tests for PR details fetching, mocking `gh` CLI calls.
    *   [ ] Sub-task: Write unit tests for PR diff data fetching.
    *   [ ] Sub-task: Write unit tests for branch comparison logic.
*   **Task: Update `pyproject.toml`**
    *   [ ] Sub-task: Add any new dependencies required by the `PRManager` extensions.
        *   Files: `pyproject.toml`
*   **Task: Local Quality Checks**
    *   [ ] Sub-task: Run `uv run ruff check .` and `uv run ruff format .` on affected files.
    *   [ ] Sub-task: Run `uv run mypy .` on affected files.
    *   [ ] Sub-task: Ensure all unit tests (`uv run pytest tests/unit`) pass and maintain >80% coverage.
*   [ ] Task: Conductor - User Manual Verification 'Command Layer Development (Agent A) - PR Data Fetching' (Protocol in workflow.md)

### Phase 2: Model Definition (Agent B) - Structured PR Review Data

**Objective:** Define Pydantic models to structure the input and output data for the `pr_review` feature.

*   **Task: Define PR Review Input Models**
    *   [ ] Sub-task: Create a Pydantic model for `PrReviewInput` (e.g., `repo_name`, `pr_id`, `target_branch`, `review_depth`).
        *   Files: `src/gh_wrapper/models/pr_review.py` (new)
    *   [ ] Sub-task: Update `src/gh_wrapper/models/__init__.py` to expose `pr_review` models.
        *   Files: `src/gh_wrapper/models/__init__.py`
*   **Task: Define PR Review Output Models**
    *   [ ] Sub-task: Create Pydantic models for `PrSummary` (modified files, key diffs).
        *   Files: `src/gh_wrapper/models/pr_review.py`
    *   [ ] Sub-task: Create Pydantic models for `SuggestedComment` (text, severity, location, type).
        *   Files: `src/gh_wrapper/models/pr_review.py`
    *   [ ] Sub-task: Create a top-level Pydantic model for `PrReviewOutput` (combining summary, comments, metrics).
        *   Files: `src/gh_wrapper/models/pr_review.py`
*   **Task: Update `pyproject.toml`**
    *   [ ] Sub-task: Add any new dependencies required by the `pr_review` models (unlikely for `pydantic` if already present).
        *   Files: `pyproject.toml`
*   **Task: Local Quality Checks**
    *   [ ] Sub-task: Run `uv run ruff check .` and `uv run ruff format .` on affected files.
    *   [ ] Sub-task: Run `uv run mypy .` on affected files.
    *   [ ] Sub-task: Ensure the new models validate correctly.
*   [ ] Task: Conductor - User Manual Verification 'Model Definition (Agent B) - Structured PR Review Data' (Protocol in workflow.md)

### Phase 3: Feature Layer Development (Agent B) - `PrReviewAnalyzer`

**Objective:** Implement the core logic for the `pr_review` feature, orchestrating data fetching and analysis.

*   **Task: Implement `PrReviewAnalyzer` Class**
    *   [ ] Sub-task: Create `PrReviewAnalyzer` class in `src/gh_wrapper/features/pr_review_analyzer.py`.
        *   Files: `src/gh_wrapper/features/pr_review_analyzer.py` (new)
    *   [ ] Sub-task: Initialize `PrReviewAnalyzer` with necessary command managers (e.g., `PRManager`).
    *   [ ] Sub-task: Integrate `RepoContextAnalyzer` to allow cross-referencing PR changes with the overall repository structure.
    *   [ ] Sub-task: Update `src/gh_wrapper/features/__init__.py` to expose `pr_review_analyzer`.
        *   Files: `src/gh_wrapper/features/__init__.py`
*   **Task: Implement `analyze_pr` Method**
    *   [ ] Sub-task: Implement method to accept `PrReviewInput` model.
    *   [ ] Sub-task: Call `PRManager` to fetch raw PR data based on input.
    *   [ ] Sub-task: Implement Diff Parsing: Parse the raw diff output from `gh pr diff --patch` into a structured format, mapping changes to `FileChange` models (from Phase 2) using a library like unidiff or a robust regex-based parser.
    *   [ ] Sub-task: Process raw data to generate `PrSummary`.
    *   [ ] Sub-task: Implement logic to identify patterns for `SuggestedComment` generation (e.g., regex for common issues, basic code style checks on diffs).
    *   [ ] Sub-task: Construct `PrReviewOutput` model from processed data.
*   **Task: Implement `format_as_markdown` Method**
    *   [ ] Sub-task: Create a method to take `PrReviewOutput` and format it into a human-readable Markdown string.
*   **Task: Write Unit Tests for `PrReviewAnalyzer`**
    *   [ ] Sub-task: Create `test_pr_review_analyzer.py`.
        *   Files: `tests/unit/features/test_pr_review_analyzer.py` (new)
    *   [ ] Sub-task: Write unit tests for `analyze_pr` method, mocking `PRManager` calls.
    *   [ ] Sub-task: Write unit tests for `format_as_markdown` method.
*   **Task: Local Quality Checks**
    *   [ ] Sub-task: Run `uv run ruff check .` and `uv run ruff format .` on affected files.
    *   [ ] Sub-task: Run `uv run mypy .` on affected files.
    *   [ ] Sub-task: Ensure all unit tests (`uv run pytest tests/unit`) pass and maintain >80% coverage.
*   [ ] Task: Conductor - User Manual Verification 'Feature Layer Development (Agent B) - `PrReviewAnalyzer`' (Protocol in workflow.md)

### Phase 4: Integration & Refinement (Both Agents/Shared)

**Objective:** Ensure end-to-end functionality, validate the feature with integration tests, and provide a usage example.

*   **Task: Write Integration Tests for `pr_review` Feature**
    *   [ ] Sub-task: Create `test_pr_review_integration.py`.
        *   Files: `tests/integration/test_pr_review_integration.py` (new)
    *   [ ] Sub-task: Write integration tests that invoke `PrReviewAnalyzer` with real `gh` CLI calls.
    *   [ ] Sub-task: Verify both JSON and Markdown outputs against expected results.
*   **Task: Create Demo Script**
    *   [ ] Sub-task: Create `demo_pr_review.py` demonstrating how to use the new feature.
        *   Files: `scripts/demo_pr_review.py` (new)
    *   [ ] Sub-task: Include example usage for both structured JSON and formatted Markdown output.
*   **Task: Documentation Updates**
    *   [ ] Sub-task: Update `README.md` with a brief mention of the new feature.
    *   [ ] Sub-task: Add a usage example to `docs/Usage_example.md`.
*   **Task: Final Quality Checks**
    *   [ ] Sub-task: Run all tests (`uv run pytest`).
    *   [ ] Sub-task: Ensure overall unit test coverage is >80%.
    *   [ ] Sub-task: Run `uv run ruff check .`, `uv run ruff format .`, and `uv run mypy .` on the entire project.
*   [ ] Task: Conductor - User Manual Verification 'Integration & Refinement (Both Agents/Shared)' (Protocol in workflow.md)
