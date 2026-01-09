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
