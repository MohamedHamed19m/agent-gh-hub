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
