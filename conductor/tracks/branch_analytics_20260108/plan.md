# Plan: Branch Analytics Feature

## Phase 1: Core Implementation & Unit Tests
- [ ] Task: Create `BranchAnalyzer` class structure and Pydantic models in `src/gh_wrapper/features/branch_analytics.py`.
    -   *Context:* Define `BranchStats` model.
    -   *Workflow:* TDD - Write `tests/unit/features/test_branch_analytics.py` skeleton first.
- [ ] Task: Implement `analyze_branch` logic with unit tests.
    -   *Context:* Use `GHExecutor` to fetch commits (`gh api` or `gh search`). Calculate metrics.
    -   *Workflow:* Mock `GHExecutor.run`. Verify parsing logic. Coverage > 80%.
- [ ] Task: Conductor - User Manual Verification 'Core Implementation & Unit Tests' (Protocol in workflow.md)

## Phase 2: Integration & Polish
- [ ] Task: Write Integration Tests for `BranchAnalytics`.
    -   *Context:* `tests/integration/test_branch_analytics_integration.py`.
    -   *Workflow:* Use real `GH_TOKEN`. Assert valid fields (not exact values as they change).
- [ ] Task: Update `README.md` and `scripts/demo_usage.py`.
    -   *Context:* Add documentation and a live demo example.
- [ ] Task: Conductor - User Manual Verification 'Integration & Polish' (Protocol in workflow.md)
