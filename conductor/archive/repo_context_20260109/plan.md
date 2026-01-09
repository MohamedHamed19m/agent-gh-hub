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
