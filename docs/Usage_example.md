# Usage Examples

## File Manager Demo
The `scripts/demo_file_manager.py` script demonstrates the core capabilities of the `FileManager` class. It is designed to be dynamic and works out-of-the-box with any repository.

### Prerequisites
- **GitHub CLI:** Installed and authenticated (`gh auth login`).
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
