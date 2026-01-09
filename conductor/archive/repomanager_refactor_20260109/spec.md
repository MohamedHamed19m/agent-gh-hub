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
