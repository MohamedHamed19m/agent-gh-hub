from unittest.mock import MagicMock
from typing import Any, Dict, List # Added import for List and Any

import pytest

# Assuming GHExecutor is defined elsewhere and has an 'execute' method.
# For testing purposes, we'll mock it.
# If GHExecutor is in a specific module, you might need to import it like:
# from src.gh_wrapper.core.executor import GHExecutor
# For now, we'll use a placeholder or assume it's available in scope for the mock.


class GHExecutor:  # Placeholder for type hinting and mocking purposes
    def execute(self, command: List[str], parse_json: bool = True) -> Any:
        pass


@pytest.fixture
def mock_executor():
    """Mock GHExecutor for all tests."""
    mock = MagicMock(spec=GHExecutor)
    # Provide a default return value for execute if needed, or let tests set it.
    # For example: mock.execute.return_value = None
    return mock


def test_list_prs(mock_executor):
    """Test PRManager.list_prs with mocked executor."""
    mock_pr_list_return = [
        {
            "number": 1,
            "title": "feat: Initial commit",
            "url": "http://...",
            "author": "user",
            "createdAt": "...",
            "state": "open",
            "headRefName": "feat-branch",
            "baseRefName": "main",
        },
        {
            "number": 2,
            "title": "fix: Bug fix",
            "url": "http://...",
            "author": "user",
            "createdAt": "...",
            "state": "closed",
            "headRefName": "bug-fix",
            "baseRefName": "main",
        },
    ]
    mock_executor.execute.return_value = mock_pr_list_return

    # Assuming PRManager is in src.gh_wrapper.commands.pull_requests
    # If the path is different, adjust the import.
    from src.gh_wrapper.commands.pull_requests import PRManager

    pr_manager = PRManager(mock_executor)

    prs = pr_manager.list_prs(state="open", limit=5)

    expected_cmd = [
        "pr",
        "list",
        "--state",
        "open",
        "--limit",
        "5",
        "--json",
        "number,title,url,author,createdAt,state,headRefName,baseRefName",
    ]
    mock_executor.execute.assert_called_once_with(expected_cmd, parse_json=True)
    assert len(prs) == 2
    assert prs[0]["number"] == 1
    assert prs[1]["state"] == "closed"


def test_list_prs_empty(mock_executor):
    """Test PRManager.list_prs when no PRs are returned."""
    mock_executor.execute.return_value = []

    from src.gh_wrapper.commands.pull_requests import PRManager

    pr_manager = PRManager(mock_executor)
    prs = pr_manager.list_prs()

    expected_cmd = [
        "pr",
        "list",
        "--state",
        "open",
        "--limit",
        "10",
        "--json",
        "number,title,url,author,createdAt,state,headRefName,baseRefName",
    ]
    mock_executor.execute.assert_called_once_with(expected_cmd, parse_json=True)
    assert prs == []


def test_get_pr_content(mock_executor):
    """Test PRManager.get_pr_content with mocked executor."""
    mock_pr_view_return = {
        "number": 123,
        "title": "feat: Add new feature",
        "body": "This PR adds a new feature.",
        "comments": 5,
        "reviews": 2,
        "files": [{"path": "src/main.py", "additions": 10, "deletions": 2}],
    }
    mock_executor.execute.return_value = mock_pr_view_return

    from src.gh_wrapper.commands.pull_requests import PRManager

    pr_manager = PRManager(mock_executor)
    content = pr_manager.get_pr_content(123)

    expected_cmd = [
        "pr",
        "view",
        "123",
        "--json",
        "number,title,body,comments,reviews,files",
    ]
    mock_executor.execute.assert_called_once_with(expected_cmd, parse_json=True)
    assert content["number"] == 123
    assert content["title"] == "feat: Add new feature"
    assert len(content["files"]) == 1


def test_get_pr_content_empty(mock_executor):
    """Test PRManager.get_pr_content when no content is returned."""
    mock_executor.execute.return_value = {}

    from src.gh_wrapper.commands.pull_requests import PRManager

    pr_manager = PRManager(mock_executor)
    content = pr_manager.get_pr_content(999)

    expected_cmd = [
        "pr",
        "view",
        "999",
        "--json",
        "number,title,body,comments,reviews,files",
    ]
    mock_executor.execute.assert_called_once_with(expected_cmd, parse_json=True)
    assert content == {}


def test_get_pr_diff(mock_executor):
    """Test PRManager.get_pr_diff with mocked executor."""
    mock_diff_output = """
diff --git a/src/file1.py b/src/file1.py
index abcdefg..hijklmn 100644
--- a/src/file1.py
+++ b/src/file1.py
@@ -1,5 +1,6 @@
 def hello_world():
     print("Hello, world!")
+    print("New line added.")
 """
    mock_executor.execute.return_value = mock_diff_output

    from src.gh_wrapper.commands.pull_requests import PRManager

    pr_manager = PRManager(mock_executor)
    diff = pr_manager.get_pr_diff(pr_number=456)

    expected_cmd = ["pr", "diff", "456", "--patch"]
    mock_executor.execute.assert_called_once_with(expected_cmd, parse_json=False)
    assert diff == mock_diff_output
    assert "New line added." in diff


def test_get_pr_diff_with_target_branch(mock_executor):
    """Test PRManager.get_pr_diff with a target branch."""
    mock_diff_output = """
diff --git a/src/file2.py b/src/file2.py
index abcdefg..hijklmn 100644
--- a/src/file2.py
+++ b/src/file2.py
@@ -1,3 +1,4 @@
 def goodbye():
     print("Goodbye")
+    # This is a test comment
 """
    mock_executor.execute.return_value = mock_diff_output

    from src.gh_wrapper.commands.pull_requests import PRManager

    pr_manager = PRManager(mock_executor)
    diff = pr_manager.get_pr_diff(pr_number=789, target_branch="main")

    expected_cmd = ["pr", "diff", "789", "--patch", "--base", "main"]
    mock_executor.execute.assert_called_once_with(expected_cmd, parse_json=False)
    assert diff == mock_diff_output
    assert "# This is a test comment" in diff


def test_get_pr_diff_empty(mock_executor):
    """Test PRManager.get_pr_diff when no diff is returned."""
    mock_executor.execute.return_value = ""

    from src.gh_wrapper.commands.pull_requests import PRManager

    pr_manager = PRManager(mock_executor)
    diff = pr_manager.get_pr_diff(pr_number=101)

    expected_cmd = ["pr", "diff", "101", "--patch"]
    mock_executor.execute.assert_called_once_with(expected_cmd, parse_json=False)
    assert diff == ""


# Note: The GHExecutor class itself is not provided, so we are mocking its interface.
# If GHExecutor has specific initialization or methods that need mocking,
# this fixture might need to be adjusted.
