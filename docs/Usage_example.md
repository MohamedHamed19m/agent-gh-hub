# Usage Examples

## File Manager Demo
The `scripts/demo_file_manager.py` script demonstrates the core capabilities of the `FileManager` class. It is designed to be dynamic and works out-of-the-box with any repository.

### Prerequisites
- **GitHub CLI:** Installed and authenticated (`gh auth login`). 
  - **Tip:** Run `gh auth status` to ensure you are logged in to the correct account and host.
  - **Note:** You do not need to set `GH_HOST` manually; the scripts inherit your active CLI session's configuration automatically.
- **uv:** Installed for dependency management.
- **Fancy Extras:** Highly recommended for the rich terminal output.
  ```bash
  uv sync --extra fancy
  ```

### How to Run with Your Repository
To test the script on your own repository:

1.  Open `scripts/demo_file_manager.py`.
2.  Scroll to the bottom of the file to the `if __name__ == "__main__":` block.
3.  Replace the `repo_name` variable with your target repository in the format `ORG_NAME/REPO_NAME`.
    ```python
    if __name__ == "__main__":
        # Change this to your target repository
        repo_name = "YOUR_ORG/YOUR_REPO"
        demo_file_manager_capabilities(repo_name)
    ```
4.  Run the script using `uv`:
    ```bash
    uv run scripts/demo_file_manager.py
    ```

### Dynamic Capabilities
Unlike static demos, this script is fully context-aware:
- **Auto-Branch Detection:** It queries the GitHub API to find the actual default branch (e.g., `main`, `master`, or `master_integration`).
- **Auto-Path Selection:** It identifies the first directory and file in your repository's root to demonstrate the Tree view and Content reading features automatically.
- **Syntax Highlighting:** It detects file extensions to apply the correct syntax highlighting in the terminal.

## Repo Analysis Feature
Insights into commit patterns, contributor activity, and volume trends across multiple branches.

### Prerequisites
- **GitHub CLI:** Authenticated.
- **gh-wrapper:** Installed and synced.

### How to Run
Run the demo script to analyze the current repository:
```bash
uv run scripts/demo_repo_analysis.py
```

## Feature Tracer Feature
Cross-sectional insights into feature development across multiple repositories, including code mentions, commits, and PRs.

### Prerequisites
- **GitHub CLI:** Authenticated.
- **gh-wrapper:** Installed and synced.

### How to Run
Run the demo script to trace a feature keyword across repositories:
```bash
uv run scripts/demo_feature_tracer.py
```

## User Activity Tracer
Trace recent work of a specific user within a repository, providing a timeline of their contributions.

### Prerequisites
- **GitHub CLI:** Authenticated.
- **gh-wrapper:** Installed and synced.

### How to Run
Run the demo script to trace user activity:
```bash
uv run scripts/demo_trace_user_activity.py
```

## PR Review Feature
Automated change summary and review suggestions for Pull Requests, including diff analysis and metrics.

### Prerequisites
- **GitHub CLI:** Authenticated.
- **gh-wrapper:** Installed and synced.

### How to Run
Run the demo script to analyze the latest PR in a target repository:
```bash
uv run scripts/demo_pr_review.py
```