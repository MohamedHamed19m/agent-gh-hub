# Plan: Feature Tracer Implementation

## Phase 1: Models & Foundation
- [x] Task: Define Pydantic models in `src/gh_wrapper/models/trace.py`.
    - [x] Sub-task: Define `FileMatch`, `TraceCommit`, `TracePR`.
    - [x] Sub-task: Define `FeatureTrace` (single repo result).
    - [x] Sub-task: Define `MultiRepoFeatureTrace` (container).
- [x] Task: Export models in `src/gh_wrapper/models/__init__.py`.
- [ ] Task: Conductor - User Manual Verification 'Phase 1' (Protocol in workflow.md)

## Phase 2: Core Search Logic (TDD)
- [x] Task: Scaffold `FeatureTracer` class in `src/gh_wrapper/features/feature_tracer.py`.
- [x] Task: Implement `trace_feature` method (TDD).
    - [x] Sub-task: Write unit tests mocking `FileManager`, `CommitsManager`, and `PRManager`.
    - [x] Sub-task: Implement repo normalization logic.
    - [x] Sub-task: Implement search in files using `FileManager`.
    - [x] Sub-task: Implement search in commits with client-side keyword filtering.
    - [x] Sub-task: Implement search in PRs with client-side keyword filtering.
    - [x] Sub-task: Verify search toggles (`search_files`, `search_commits`, `search_prs`) are respected.
- [ ] Task: Conductor - User Manual Verification 'Phase 2' (Protocol in workflow.md)

## Phase 3: Contributor Analysis & Metadata (TDD)
- [x] Task: Implement contributor aggregation logic.
    - [x] Sub-task: Write unit tests for contributor counting from commits/PRs.
    - [x] Sub-task: Implement ranking logic (sort by activity volume).
- [x] Task: Implement trace metadata calculation.
    - [x] Sub-task: Calculate `total_mentions`, `first_mention_date`, `last_activity_date`.
- [ ] Task: Conductor - User Manual Verification 'Phase 3' (Protocol in workflow.md)

## Phase 4: Formatting & Documentation
- [x] Task: Implement `format_as_markdown` method.
    - [x] Sub-task: Write unit tests for markdown output consistency.
    - [x] Sub-task: Implement summary layout with contributor rankings.
- [x] Task: Add comprehensive docstrings and usage examples.
- [ ] Task: Conductor - User Manual Verification 'Phase 4' (Protocol in workflow.md)

## Phase 5: Integration & Final Verification
- [x] Task: Integration Testing.
    - [x] Sub-task: Create `tests/integration/test_feature_tracer_integration.py`.
    - [x] Sub-task: Verify search against a real public repository.
- [x] Task: Final Quality Check.
    - [x] Sub-task: Run full test suite (`unit` + `integration`).
    - [x] Sub-task: Verify `ruff` and `mypy` pass without errors.
- [ ] Task: Conductor - User Manual Verification 'Phase 5' (Protocol in workflow.md)
