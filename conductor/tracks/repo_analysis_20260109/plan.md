# Plan: Repo Analysis Feature Implementation

## Phase 1: Foundation & Command Extension
- [x] Task: Create Models Directory Structure.
    - [x] Sub-task: Create `src/gh_wrapper/models/` directory.
    - [x] Sub-task: Create `src/gh_wrapper/models/__init__.py`.
    - [x] Sub-task: Create `src/gh_wrapper/models/analysis.py` for `CommitAnalysisReport`.
    - [x] Sub-task: Export all models in `models/__init__.py` for cleaner imports.
- [x] Task: Extend CommitsManager (Command Layer).
    - [x] Sub-task: Add `get_commits_for_analysis(branch, since, limit)` to `src/gh_wrapper/commands/commits.py`.
    - [x] Sub-task: Ensure it returns full GitHub API response (not flattened).
    - [x] Sub-task: Write unit tests for the new method.
    - [x] Sub-task: Verify `get_commit_details()` functionality.
- [x] Task: Scaffold `RepoAnalyzer` class.
    - [x] Sub-task: Create `src/gh_wrapper/features/repo_analysis.py`.
    - [x] Sub-task: Initialize with `CommitsManager` dependency.
- [ ] Task: Conductor - User Manual Verification 'Phase 1' (Protocol in workflow.md)

## Phase 2: Core Logic Implementation
- [x] Task: Implement `analyze_commit_patterns` (TDD).
    - [x] Sub-task: Write unit tests mocking `get_commits_for_analysis` for multiple branches.
    - [x] Sub-task: Implement aggregation logic with separate helper methods:
        - `_calculate_daily_trend()` (Daily/weekly commit counts)
        - `_analyze_contributors()` (Top contributors with percentages)
        - `_analyze_time_patterns()` (By hour and by weekday)
    - [x] Sub-task: Verify tests pass with >80% coverage.
- [x] Task: Error Handling & Edge Cases.
    - [x] Sub-task: Add logging for warnings and errors.
    - [x] Sub-task: Add input validation (non-empty branches, positive days_back).
    - [x] Sub-task: Test edge cases:
        - Invalid branch names
        - Empty commit history
        - API failures (rate limits, network errors)
- [ ] Task: Conductor - User Manual Verification 'Phase 2' (Protocol in workflow.md)

## Phase 3: Output Formatting
- [ ] Task: Implement `format_as_markdown`.
    - [ ] Sub-task: Write unit tests with sample models.
    - [ ] Sub-task: Implement formatting logic for Markdown tables and lists.
- [ ] Task: Conductor - User Manual Verification 'Phase 3' (Protocol in workflow.md)

## Phase 4: Integration Testing
- [ ] Task: Integration Testing.
    - [ ] Sub-task: Create `tests/integration/test_repo_analysis_integration.py`.
    - [ ] Sub-task: Test against actual repository using `test-branch-fixture` branch.
    - [ ] Sub-task: Analyze `test-branch-fixture` (last 30 days).
    - [ ] Sub-task: Analyze multiple branches (e.g., `main`, `test-branch-fixture`).
    - [ ] Sub-task: Verify report structure and data quality.
    - [ ] Sub-task: Format report as Markdown and verify readable output.
    - [ ] Sub-task: Compare results against known commit history in test branch.
- [ ] Task: Conductor - User Manual Verification 'Phase 4' (Protocol in workflow.md)

## Phase 5: Documentation & AI Context
- [ ] Task: Documentation.
    - [ ] Sub-task: Add comprehensive docstrings to all public methods.
    - [ ] Sub-task: Add usage examples in `repo_analysis.py` module docstring.
    - [ ] Sub-task: Update `docs/Usage_example.md` with RepoAnalyzer section (Prerequisites, How to Run).
    - [ ] Sub-task: Create `scripts/demo_repo_analysis.py`.
- [ ] Task: Update AI Context Documentation (`GEMINI.md`).
    - [ ] Sub-task: Add `models/` directory to "Key Technologies" section.
    - [ ] Sub-task: Add "Project Structure" section showing `commands/`, `features/`, `models/`, `core/` hierarchy.
    - [ ] Sub-task: Add "Repo Analysis Feature" section under "Features" (Purpose, Data models, Methods, Testing).
    - [ ] Sub-task: Update "Feature Design Philosophy" with concrete RepoAnalyzer example showing Command/Feature/Models layers.
- [ ] Task: Final Verification.
    - [ ] Sub-task: Run full test suite (`unit` + `integration`).
    - [ ] Sub-task: Check `mypy` and `ruff`.
- [ ] Task: Conductor - User Manual Verification 'Phase 5' (Protocol in workflow.md)
