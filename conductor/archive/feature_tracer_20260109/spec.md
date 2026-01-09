# Specification: Feature Tracer

## Overview
The `FeatureTracer` is a specialized feature that searches across one or more repositories to provide a comprehensive, cross-sectional insight into the development of a specific feature or topic (e.g., "secure boot", "CommitsManager"). It aggregates relevant commits, pull requests, files, and contributor data to offer a unified view of how a feature evolved across the organization.

## Functional Requirements
- **Initialization:**
    - Constructor: `FeatureTracer()` (no parameters - stateless).
    - Repositories are passed per-call via `trace_feature(repos=...)`.
    - Managers are created dynamically for each repository during the search loop.

- **Search Execution:**
    - Method: `trace_feature(keyword: str, repos: Union[str, List[str]], ...) -> MultiRepoFeatureTrace`
    - **Parameters:**
        - `keyword`: The phrase to search for.
        - `repos`: Single repo string or list of repo strings. Automatically normalizes to list.
        - `branches`: List of branches to search (default: `["main"]`).
        - `since`: Optional date string (YYYY-MM-DD) to filter history.
        - **Toggles:**
            - `search_files: bool = True`
            - `search_commits: bool = True`
            - `search_prs: bool = True`
        - **Performance Limits:**
            - `max_commits_per_branch: int = 100` - Limit commits fetched per branch.

- **Search Capabilities:**
    - **Files:** Search code for keyword mentions using `FileManager.search_in_files()` (exact match, case-insensitive).
    - **Commits:** 
        - Fetch via `CommitsManager.get_commits(branch, limit, since, ...)`.
        - Filter client-side: `keyword.lower() in commit['message'].lower()`.
    - **Pull Requests:** 
        - Fetch via `PRManager.list_prs(state="all", limit, ...)` (state="all" to catch history).
        - Filter client-side: `keyword.lower() in pr['title'].lower() or pr['body'].lower()`.

- **Data Aggregation & Output:**
    - Return a `MultiRepoFeatureTrace` Pydantic model containing:
        - `keyword`: The search term used.
        - `repos_searched`: List of repository names.
        - `traces`: Dictionary mapping repo names to `FeatureTrace` objects.
    
    - `FeatureTrace` (Single Repo Result) contains:
        - `keyword`, `repo`: Identification.
        - `file_matches`: List of `FileMatch` objects (path, match snippet).
        - `commit_matches`: List of `TraceCommit` objects.
        - `pr_matches`: List of `TracePR` objects.
        - `contributors`: List[Dict[str, Any]] containing:
            - `username: str`
            - `commit_count: int`
            - `pr_count: int`
        - `metadata`: `total_mentions`, `first_mention_date`, `last_activity_date`.

- **AI-Optimized Output:**
    - Provide a `format_as_markdown` method to generate a concise, human-readable summary.

## Non-Functional Requirements
- **Performance:**
    - **V1:** Sequential execution per repository (simple, reliable).
    - **Optimization:** Future tracks may add ThreadPoolExecutor.
- **Robustness:** Gracefully handle search failures for individual repositories without failing the entire operation.
- **Type Safety:** All data structures must be defined as Pydantic models in `src/gh_wrapper/models/trace.py`.

## Acceptance Criteria
- [ ] `FeatureTracer` class implemented in `src/gh_wrapper/features/feature_tracer.py`.
- [ ] Pydantic models defined in `src/gh_wrapper/models/trace.py`.
- [ ] `trace_feature` accepts flexible repo arguments, toggles, and limits.
- [ ] Client-side filtering works correctly for Commits and PRs.
- [ ] `format_as_markdown` produces a clear summary including contributor rankings.
- [ ] Unit tests verify aggregation logic, toggles, and limits.
- [ ] Integration test runs against a real public repo.

## Out of Scope
- Issue searching.
- Deep dependency linking.
- Parallel execution (deferred).
