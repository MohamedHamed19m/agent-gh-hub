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
