
---
# File: product-guidelines.md
# Path: product-guidelines.md
---

# Product Guidelines

## Output Tone & Voice
- **Succinct & Machine-Readable:** All primary outputs intended for AI agents must prioritize token efficiency and strict JSON validity. Avoid unnecessary prose or decorative formatting in data payloads.

## Error Handling
- **Standardized Error Envelopes:** Every response from the system must follow a consistent structure. Errors must be returned as JSON objects containing an `error` field, a status code (if applicable), and a concise, actionable error message to allow agents to recover or report issues programmatically.

## Feature Design Philosophy
- **Compositional Architecture:** New high-level features should be built by composing existing low-level command wrappers. This ensures consistency in how the GitHub CLI is invoked and data is processed, while maximizing code reuse across the `gh_wrapper.features` module.

## Performance
- **Minimal Latency:** Features should be optimized for speed, as agents often operate in real-time loops. Use caching where appropriate to avoid redundant CLI calls.



---
# File: product.md
# Path: product.md
---

# Initial Concept
A robust, Pythonic wrapper around the GitHub CLI (gh), engineered specifically for AI Agents and high-automation environments.

# Product Vision
To serve as the primary "eyes and ears" for autonomous coding agents, providing them with structured, AI-optimized access to GitHub's rich repository data and workflows.

# Target Users
- Developers building autonomous coding agents.
- AI Agents (Claude, Gemini, GPT) requiring direct repository interaction.
- CI/CD pipelines needing advanced GitHub CLI automation.

# Key Features
- **Feature Tracer:** Deep search for logic across branches and repositories.
- **Repo Analysis:** High-level insights into commit volume trends, contributor activity, and time-based patterns.
- **User Activity Analytics:** Insights into developer progress and intent.
- **Repo Contextualizer:** High-level summary of repository structure and state for LLM context windows.
- **Structured API Wrappers:** Pydantic-powered interfaces for Commits, PRs, and Files.

# Success Metrics
- Seamless integration with leading LLM agent frameworks.
- Minimal latency for CLI-based data retrieval.
- High reliability across diverse GitHub Enterprise and Public environments.



---
# File: tech-stack.md
# Path: tech-stack.md
---

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



---
# File: tracks.md
# Path: tracks.md
---

﻿# Project Tracks

This file tracks all major tracks for the project. Each track has its own detailed plan in its respective folder.

---

## [x] Track: Add Branch Analytics feature
*Link: [./conductor/tracks/branch_analytics_20260108/](./conductor/tracks/branch_analytics_20260108/)*

## [x] Track: Implement Core Features
*Includes: Feature Tracer, User Tracer, Repo Context, and Advanced Commit Search.*
*Status: All core features implemented in src/gh_wrapper/features/*






---
# File: workflow.md
# Path: workflow.md
---

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


---
# File: general.md
# Path: code_styleguides\general.md
---

# General Code Style Principles

This document outlines general coding principles that apply across all languages and frameworks used in this project.

## Readability
- Code should be easy to read and understand by humans.
- Avoid overly clever or obscure constructs.

## Consistency
- Follow existing patterns in the codebase.
- Maintain consistent formatting, naming, and structure.

## Simplicity
- Prefer simple solutions over complex ones.
- Break down complex problems into smaller, manageable parts.

## Maintainability
- Write code that is easy to modify and extend.
- Minimize dependencies and coupling.

## Documentation
- Document *why* something is done, not just *what*.
- Keep documentation up-to-date with code changes.



---
# File: python.md
# Path: code_styleguides\python.md
---

# Google Python Style Guide Summary

This document summarizes key rules and best practices from the Google Python Style Guide.

## 1. Python Language Rules
- **Linting:** Run `ruff check` on your code to catch bugs and style issues.
- **Imports:** Use `import x` for packages/modules. Use `from x import y` only when `y` is a submodule.
- **Exceptions:** Use built-in exception classes. Do not use bare `except:` clauses.
- **Global State:** Avoid mutable global state. Module-level constants are okay and should be `ALL_CAPS_WITH_UNDERSCORES`.
- **Comprehensions:** Use for simple cases. Avoid for complex logic where a full loop is more readable.
- **Default Argument Values:** Do not use mutable objects (like `[]` or `{}`) as default values.
- **True/False Evaluations:** Use implicit false (e.g., `if not my_list:`). Use `if foo is None:` to check for `None`.
- **Type Annotations:** Strongly encouraged for all public APIs.

## 2. Python Style Rules
- **Line Length:** Maximum 88 characters (consistent with Ruff default).
- **Indentation:** 4 spaces per indentation level. Never use tabs.
- **Blank Lines:** Two blank lines between top-level definitions (classes, functions). One blank line between method definitions.
- **Whitespace:** Avoid extraneous whitespace. Surround binary operators with single spaces.
- **Docstrings:** Use `"""triple double quotes"""`. Every public module, function, class, and method must have a docstring.
  - **Format:** Start with a one-line summary. Include `Args:`, `Returns:`, and `Raises:` sections.
- **Strings:** Use f-strings for formatting. Be consistent with single (`'`) or double (`"`) quotes.
- **`TODO` Comments:** Use `TODO(username): Fix this.` format.
- **Imports Formatting:** Imports should be on separate lines and grouped: standard library, third-party, and your own application's imports.

## 3. Naming
- **General:** `snake_case` for modules, functions, methods, and variables.
- **Classes:** `PascalCase`.
- **Constants:** `ALL_CAPS_WITH_UNDERSCORES`.
- **Internal Use:** Use a single leading underscore (`_internal_variable`) for internal module/class members.

## 4. Main
- All executable files should have a `main()` function that contains the main logic, called from a `if __name__ == '__main__':` block.

**BE CONSISTENT.** When editing code, match the existing style.

*Source: [Google Python Style Guide](https://google.github.io/styleguide/pyguide.html)*


---
# File: plan.md
# Path: tracks\branch_analytics_20260108\plan.md
---

# Plan: Branch Analytics Feature

## Phase 1: Core Implementation & Unit Tests
- [x] Task: Create `BranchAnalyzer` class structure and Pydantic models in `src/gh_wrapper/features/branch_analytics.py`.
    -   *Context:* Define `BranchStats` model.
    -   *Workflow:* TDD - Write `tests/unit/features/test_branch_analytics.py` skeleton first.
- [x] Task: Implement `analyze_branch` logic with unit tests.
    -   *Context:* Use `GHExecutor` to fetch commits (`gh api` or `gh search`). Calculate metrics.
    -   *Workflow:* Mock `GHExecutor.run`. Verify parsing logic. Coverage > 80%.
- [x] Task: Conductor - User Manual Verification 'Core Implementation & Unit Tests' (Protocol in workflow.md)
    -   *Checkpoint:* `8fec8a33202ae9ca4dcafa46a2b80c277b1a0c34`

## Phase 2: Integration & Polish
- [x] Task: Write Integration Tests for `BranchAnalytics`.
    -   *Context:* `tests/integration/test_branch_analytics_integration.py`.
    -   *Workflow:* Use real `GH_TOKEN`. Assert valid fields (not exact values as they change).
- [x] Task: Update `README.md` and `scripts/demo_usage.py`.
    -   *Context:* Add documentation and a live demo example.
- [x] Task: Conductor - User Manual Verification 'Integration & Polish' (Protocol in workflow.md)
    -   *Checkpoint:* `b64ae1a1dcf2cee9916ac21bf7f8d04404d65d45`



---
# File: spec.md
# Path: tracks\branch_analytics_20260108\spec.md
---

# Specification: Branch Analytics Feature

## 1. Overview
The "Branch Analytics" feature provides a high-level statistical overview of one or more branches. It is designed to help AI agents understand the "health" and activity level of a branch without parsing thousands of individual commits. It leverages the existing `GHExecutor` and `Compositional Architecture` principles.

## 2. User Stories
-   **As an AI Agent**, I want to know how active a branch is (commit frequency, last update) so I can prioritize relevant context.
-   **As a Developer**, I want to identify the top contributors on a branch to know who to ping for reviews.
-   **As a CI Pipeline**, I want to detect stale branches that haven't been touched in X days.

## 3. Key Metrics (Output)
The feature will return a JSON object containing:
-   **Branch Name:** Target branch.
-   **Total Commits:** (In the scanned period/limit).
-   **Last Commit:** Timestamp and Author.
-   **Contributors:** List of unique authors with commit counts.
-   **Activity:** Breakdown of commits by day/week (optional, keep simple for V1).
-   **Divergence:** (Optional V2) How far ahead/behind `main` it is.

## 4. Architecture Design
-   **Module:** `gh_wrapper.features.branch_analytics`
-   **Class:** `BranchAnalyzer`
-   **Dependencies:**
    -   `GHExecutor` (for raw `gh` calls).
    -   `gh_wrapper.commands.commits` (to fetch commit lists).
    -   `gh_wrapper.commands.repository` (to validate branch existence).

## 5. API Interface
```python
class BranchAnalyzer:
    def __init__(self, executor: GHExecutor):
        ...

    def analyze_branch(self, branch: str, limit: int = 100) -> BranchStats:
        """
        Analyzes the given branch and returns statistics.
        """
        ...
```

## 6. Testing Strategy
-   **Unit Tests:** Mock `GHExecutor` responses (raw JSON from `gh log`) and verify `BranchStats` calculation.
-   **Integration Tests:** Run against a real public repo (e.g., `git/git` or `python/cpython` or self) and verify structure matches.

## 7. Documentation
-   Update `README.md` with a usage example.
-   Add a new section to `scripts/demo_usage.py` to showcase the feature.



---
# File: plan.md
# Path: archive\repomanager_refactor_20260109\plan.md
---

# Plan: RepoManager Refactor & Layer Separation

## Phase 1: Foundation & Cleanup
- [x] Task: Update `RepoManager.__init__`.
    - [x] Sub-task: Remove `PRManager` and `FileManager` instantiation.
    - [x] Sub-task: Add `max_concurrent: int = 6` parameter.
- [x] Task: Remove cross-manager dependencies.
    - [x] Sub-task: Remove `PRManager` and `FileManager` imports from `repository.py`.
- [x] Task: Extract orchestration logic.
    - [x] Sub-task: Remove `get_context()` method and replace with TODO comment.
- [x] Task: Conductor - User Manual Verification 'Phase 1' (Protocol in workflow.md)

## Phase 2: Interface Exposure & Typos
- [x] Task: Refactor and expose helper methods.
    - [x] Sub-task: Rename `_get_repo_basics` to `get_repo_basics`.
    - [x] Sub-task: Rename `_get_file_strcture` to `get_file_structure` (fix typo).
    - [x] Sub-task: Rename `_get_recent_commits` to `get_recent_commits`.
- [x] Task: Update internal calls.
    - [x] Sub-task: Update all references within `RepoManager` to use the new public method names.
- [x] Task: Documentation & Types.
    - [x] Sub-task: Add Google-style docstrings to all refactored public methods.
    - [x] Sub-task: Ensure full type hint coverage.
- [x] Task: Conductor - User Manual Verification 'Phase 2' (Protocol in workflow.md)

## Phase 3: Concurrency Implementation
- [x] Task: Implement threaded branch fetching (TDD).
    - [x] Sub-task: Refactor `get_priority_branches` to use `ThreadPoolExecutor`.
    - [x] Sub-task: Implement robust worker with `try/except` for partial failure handling.
    - [x] Sub-task: Verify `max_concurrent` is respected.
- [x] Task: Conductor - User Manual Verification 'Phase 3' (Protocol in workflow.md)

## Phase 4: Testing & Demo Update
- [x] Task: Unit Testing.
    - [x] Sub-task: Update `tests/unit/commands/test_repository.py` to cover refactored methods.
    - [x] Sub-task: Add tests for threaded execution and failure scenarios.
    - [x] Sub-task: Verify >80% coverage.
- [x] Task: Handle breaking changes in demos.
    - [x] Sub-task: Comment out `scripts/demo_read_repo_context.py` with an explanatory header.
- [x] Task: Conductor - User Manual Verification 'Phase 4' (Protocol in workflow.md)

## Phase 5: Final Verification
- [x] Task: Run full test suite.
- [x] Task: Run `ruff check` and `mypy`.
- [x] Task: Conductor - User Manual Verification 'Phase 5' (Protocol in workflow.md)



---
# File: spec.md
# Path: archive\repomanager_refactor_20260109\spec.md
---

# Specification: RepoManager Refactor & Layer Separation

## Overview
This track implements an architectural cleanup of `RepoManager` in `src/gh_wrapper/commands/repository.py`. We are enforcing the **Golden Rule**: the Command layer must be a pure, lightweight wrapper for GitHub CLI operations, devoid of orchestration logic or cross-manager dependencies. Orchestration is strictly reserved for the Feature layer.

## Functional Requirements
- **Strict Decoupling:**
    - Remove all references to `PRManager` and `FileManager` (no imports, no instantiation in `__init__`, and no method calls).
- **Extraction of Orchestration:**
    - Remove the `get_context()` method from `RepoManager`.
    - Add a `TODO` comment at the removal site referencing the future `features/repo_context.py` track.
- **Interface Exposure (Private → Public):**
    - Promote the following helpers to public APIs with standard naming and Google-style docstrings:
        - `_get_repo_basics()` -> `get_repo_basics()` (Returns metadata: branch, description, release).
        - `_get_file_strcture()` -> `get_file_structure()` (Fixing typo, returns full tree structure).
        - `_get_recent_commits()` -> `get_recent_commits()` (Returns lightweight activity summary).
- **Concurrency Control:**
    - Add `max_concurrent: int = 6` parameter to `RepoManager.__init__` to control parallel branch fetching.
    - Implement threaded execution in `get_priority_branches()` using `concurrent.futures.ThreadPoolExecutor`.
    - **Robustness:** Use `as_completed` or wrap the inner worker function in a `try/except` block to ensure that a single CLI command failure does not kill the entire batch operation. Partial results (from successful branches) should be returned.

## Non-Functional Requirements
- **Test Coverage:** Unit tests MUST achieve >80% coverage for all refactored/new methods, including mocked threaded execution scenarios.
- **Typing & Docs:** Full type hint coverage and comprehensive docstrings for all public methods.
- **Backward Compatibility:** `max_concurrent` should be optional in `__init__` to avoid breaking existing instantiations where possible, but internal calls must be updated.

## Migration Notes
- **BREAKING CHANGE:** `get_context()` is removed. Callers requiring high-level repository summaries must migrate to the future `RepoContextAnalyzer` feature.
- **Method Renaming:** Internal callers of `_get_repo_basics` etc. must be updated to use the new public names.
- **Demo Script Impact:** `scripts/demo_read_repo_context.py` will be temporarily commented out until the `RepoContextAnalyzer` feature is implemented.

## Testing Strategy
- **Unit Tests:**
    - Mock `GHExecutor.execute()` for all public methods.
    - Test `ThreadPoolExecutor` implementation using mocked branch fetches.
    - Verify `max_concurrent` actually limits the thread count.
    - Test edge cases: invalid branches, empty history, and partial CLI failures.
- **Integration Tests (Optional):**
    - Benchmark comparison: Verify threaded fetching is faster than the previous sequential approach.

## Acceptance Criteria
- [ ] `RepoManager` contains zero references to other managers.
- [ ] `get_context()` is removed with a TODO left behind.
- [ ] Typo `_get_file_strcture` is fixed to `get_file_structure`.
- [ ] `get_priority_branches` successfully runs in parallel up to `max_concurrent` threads.
- [ ] Unit tests achieve >80% coverage and pass successfully.
- [ ] `scripts/demo_read_repo_context.py` is commented out with an explanatory header.

## Out of Scope
- Re-implementing the "Repo Context" feature (reserved for a future Feature-layer track).
- Adding complex retry logic for failed threads (basic exception handling is sufficient).



---
# File: plan.md
# Path: archive\repo_analysis_20260109\plan.md
---

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
- [x] Task: Implement `format_as_markdown`.
    - [x] Sub-task: Write unit tests with sample models.
    - [x] Sub-task: Implement formatting logic for Markdown tables and lists.
- [ ] Task: Conductor - User Manual Verification 'Phase 3' (Protocol in workflow.md)

## Phase 4: Integration Testing
- [x] Task: Integration Testing.
    - [x] Sub-task: Create `tests/integration/test_repo_analysis_integration.py`.
    - [x] Sub-task: Test against actual repository using `test-branch-fixture` branch.
    - [x] Sub-task: Analyze `test-branch-fixture` (last 30 days).
    - [x] Sub-task: Analyze multiple branches (e.g., `main`, `test-branch-fixture`).
    - [x] Sub-task: Verify report structure and data quality.
    - [x] Sub-task: Format report as Markdown and verify readable output.
    - [x] Sub-task: Compare results against known commit history in test branch.
- [ ] Task: Conductor - User Manual Verification 'Phase 4' (Protocol in workflow.md)

## Phase 5: Documentation & AI Context
- [x] Task: Documentation.
    - [x] Sub-task: Add comprehensive docstrings to all public methods.
    - [x] Sub-task: Add usage examples in `repo_analysis.py` module docstring.
    - [x] Sub-task: Update `docs/Usage_example.md` with RepoAnalyzer section (Prerequisites, How to Run).
    - [x] Sub-task: Create `scripts/demo_repo_analysis.py`.
- [x] Task: Update AI Context Documentation (`GEMINI.md`).
    - [x] Sub-task: Add `models/` directory to "Key Technologies" section.
    - [x] Sub-task: Add "Project Structure" section showing `commands/`, `features/`, `models/`, `core/` hierarchy.
    - [x] Sub-task: Add "Repo Analysis Feature" section under "Features" (Purpose, Data models, Methods, Testing).
    - [x] Sub-task: Update "Feature Design Philosophy" with concrete RepoAnalyzer example showing Command/Feature/Models layers.
- [x] Task: Final Verification.
    - [x] Sub-task: Run full test suite (`unit` + `integration`).
    - [x] Sub-task: Check `mypy` and `ruff`.
- [ ] Task: Conductor - User Manual Verification 'Phase 5' (Protocol in workflow.md)



---
# File: spec.md
# Path: archive\repo_analysis_20260109\spec.md
---

# Specification: Repo Analysis Feature

## Overview
The `RepoAnalysis` feature provides high-level insights into repository activity by analyzing commit patterns across one or more branches. It bridges the gap between raw commit data and actionable intelligence for both AI agents and human developers.

## Functional Requirements
- **Commit Pattern Analysis:**
    - Analyze commits from an explicit list of branches.
    - Support a configurable lookback period (default 30 days).
    - Aggregate data for:
        - **Commit Volume Trends:** Daily/weekly counts.
        - **Contributor Activity:** Number of commits per author.
        - **Time-based Patterns:** Identification of most active days/hours.
- **Output Formats:**
    - **Programmatic:** Return data as Pydantic models (e.g., `CommitAnalysisReport`) for type-safe integration.
    - **Human-Readable:** Provide a `format_as_markdown(data)` method to generate structured summaries suitable for CLI display or LLM context.
- **Integration:**
    - Leverage existing `CommitsManager` (or `commits` command wrapper) to fetch raw data.

## Non-Functional Requirements
- **Performance:** Minimize CLI calls by batching requests or using efficient filters where possible.
- **Robustness:** Gracefully handle cases where branches do not exist or have no history within the lookback period.

## Acceptance Criteria
- [ ] `RepoAnalyzer` class implemented in `src/gh_wrapper/features/repo_analysis.py`.
- [ ] `analyze_commit_patterns` method returns a Pydantic model containing the specified metrics.
- [ ] `format_as_markdown` method correctly converts the Pydantic model into a readable Markdown report.
- [ ] Unit tests cover various scenarios (multiple branches, no commits, single branch) with >80% coverage.
- [ ] Integration tests verify functionality against a real repository.

## Out of Scope
- Code churn analysis (lines added/removed) - deferred to a future track.
- Automated branch discovery (all active branches) - requires explicit list for now.
- Visualization (graphs/charts) - only text-based output.



---
# File: plan.md
# Path: archive\repo_context_20260109\plan.md
---

# Plan: Repo Context Analyzer

## Phase 1: Foundation & Metadata
- [x] Task: Scaffold `RepoContextAnalyzer` and dependencies.
    - [x] Sub-task: Update `src/gh_wrapper/features/repo_context.py`.
    - [x] Sub-task: Initialize with `RepoManager`, `PRManager`, `FileManager`.
- [x] Task: Implement Metadata Gathering.
    - [x] Sub-task: Enhance `get_repo_basics` or implement extended metadata logic (stars, topics, fork status).
- [x] Task: Conductor - User Manual Verification 'Phase 1' (Protocol in workflow.md)

## Phase 2: Smart File Structure
- [x] Task: Implement File Tree Analysis.
    - [x] Sub-task: Implement `_is_priority_file` with the defined whitelist.
    - [x] Sub-task: Implement truncation logic (depth=2, max=20) with markers.
    - [x] Sub-task: Ensure priority files are preserved even if depth/limit exceeded.
    - [x] Sub-task: Unit tests for truncation and priority logic.
- [x] Task: Conductor - User Manual Verification 'Phase 2' (Protocol in workflow.md)

## Phase 3: Activity & Stats
- [x] Task: Implement Activity Summarization.
    - [x] Sub-task: Fetch and format last 10 commits (add branch, is_merge).
    - [x] Sub-task: Fetch and format last 10 open PRs (add status, labels, draft).
    - [x] Sub-task: Implement `Summary Stats` calculation (commits last 7d, etc.).
- [x] Task: Conductor - User Manual Verification 'Phase 3' (Protocol in workflow.md)

## Phase 4: Integration & Readme
- [x] Task: Implement README Retrieval.
    - [x] Sub-task: Fetch `README.md`, truncate to 2000 chars, strip whitespace.
- [x] Task: Orchestrate `analyze_current_context`.
    - [x] Sub-task: Assemble metadata, structure, activity, and readme into final dict.
- [x] Task: Enable Demo Script.
    - [x] Sub-task: Uncomment and update `scripts/demo_read_repo_context.py` to match new output structure.
- [x] Task: Conductor - User Manual Verification 'Phase 4' (Protocol in workflow.md)

## Phase 5: Verification
- [x] Task: Final Testing.
    - [x] Sub-task: Run full test suite.
    - [x] Sub-task: Verify `ruff` and `mypy` compliance.
- [x] Task: Conductor - User Manual Verification 'Phase 5' (Protocol in workflow.md)



---
# File: spec.md
# Path: archive\repo_context_20260109\spec.md
---

# Specification: Repo Context Analyzer

## Overview
The `RepoContextAnalyzer` feature generates a high-level, AI-optimized snapshot of a repository's current state. It bridges the gap between raw data and actionable context by intelligently summarizing file structures, prioritizing critical configuration files, and aggregating recent activity. This feature is designed to be the "first step" for any AI agent entering a codebase.

## Functional Requirements
- **Orchestration:**
    - Compose `RepoManager`, `PRManager`, and `FileManager` to fetch data.
    - Implement `analyze_current_context(branch: Optional[str])` as the main entry point.

- **Repository Metadata:**
    - Include: description, default branch, latest release tag.
    - Extended Metadata: total stars/forks (if available), fork status, archived status, topics/tags.

- **Smart File Structure:**
    - **Truncation:** Limit file tree to a configurable depth (default: 2) and max items per level (default: 20).
    - **Output Format:** Return a list of dictionaries: `{"path": str, "type": "file"|"dir"|"truncated", "priority": bool}`.
    - **Truncation Markers:** If limits exceeded, add: `{"path": "...", "type": "truncated", "count": N}`.
    - **Priority Whitelist:** Always include critical files regardless of depth:
        - Config: `pyproject.toml`, `setup.py`, `package.json`, `tsconfig.json`
        - Docker: `Dockerfile`, `docker-compose.yml`, `.dockerignore`
        - CI/CD: `.github/workflows/*`, `.gitlab-ci.yml`, `Jenkinsfile`
        - Docs: `README.md`, `CHANGELOG.md`, `CONTRIBUTING.md`, `LICENSE`
        - Other: `.gitignore`, `Makefile`

- **Activity Summarization:**
    - **Commits:** Fetch the last 10 commits. Structure: `{"sha": str, "message": str, "author": str, "date": str, "branch": str, "is_merge": bool}`.
    - **Pull Requests:** Fetch the last 10 open PRs. Structure: `{"number": int, "title": str, "author": str, "status": str, "created_at": str, "labels": List[str], "draft": bool}`.
    - **PR Status:** Enhance PR data with human-readable status (e.g., "Draft", "Ready to merge", "Changes requested", "Awaiting review").
    - **Summary Stats:** Include aggregate metrics: `{"commits_last_7d": int, "open_prs_count": int, "active_contributors_last_7d": int}` (calculated from available data or lightweight queries).

- **Content Previews:**
    - **README:** Include the first 2000 characters of `README.md`. If not found, return `None` with a note. Preserve markdown formatting but strip excessive whitespace.

## Non-Functional Requirements
- **Performance:** Context generation should take < 3 seconds for a typical repo. Use `RepoManager`'s threaded fetching where applicable.
- **Robustness:** Gracefully handle missing files or empty histories.
- **AI-Optimized:** Output format must be strictly JSON-serializable and minimize token usage.

## Acceptance Criteria
- [ ] `RepoContextAnalyzer` class implemented in `src/gh_wrapper/features/repo_context.py`.
- [ ] `_is_priority_file` correctly identifies whitelisted files.
- [ ] File tree truncation works (depth=2, max=20) while preserving priority files.
- [ ] Metadata includes stars, forks, topics, etc.
- [ ] Activity section includes enhanced Commit and PR details.
- [ ] `scripts/demo_read_repo_context.py` is uncommented and functional.
- [ ] Unit tests cover truncation, priority logic, and aggregation.

## Out of Scope
- Dependency tree analysis (parsing `package.json` vs `pyproject.toml` content).
- Issue tracking (focus is on code/PRs for now).
- Deep diff analysis of PRs.


