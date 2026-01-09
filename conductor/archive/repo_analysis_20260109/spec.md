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
