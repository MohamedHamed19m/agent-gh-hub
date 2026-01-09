import pytest
from unittest.mock import MagicMock
from typing import Any, Dict, List

from src.gh_wrapper.commands.pull_requests import PRManager
from src.gh_wrapper.core.executor import GHExecutor

# Mock GHExecutor for unit tests
@pytest.fixture
def mock_executor(mocker) -> MagicMock:
    return mocker.Mock(spec=GHExecutor)

def test_pr_manager_list_prs(mock_executor: MagicMock):
    """Test PRManager.list_prs with mocked executor."""
    expected_prs = [
        {
            "number": 1,
            "title": "Fix bug #123",
            "url": "http://example.com/pr/1",
            "author": {"login": "user1"},
            "createdAt": "2023-01-01T10:00:00Z",
            "state": "OPEN",
            "headRefName": "feature-branch-1",
            "baseRefName": "main",
        },
        {
            "number": 2,
            "title": "Add new feature",
            "url": "http://example.com/pr/2",
            "author": {"login": "user2"},
            "createdAt": "2023-01-02T11:00:00Z",
            "state": "MERGED",
            "headRefName": "feature-branch-2",
            "baseRefName": "main",
        },
    ]
    mock_executor.execute.return_value = expected_prs

    pr_manager = PRManager(mock_executor)
    prs = pr_manager.list_prs(state="open", limit=5)

    assert prs == expected_prs
    mock_executor.execute.assert_called_once_with(
        [
            "pr",
            "list",
            "--state",
            "open",
            "--limit",
            "5",
            "--json",
            "number,title,url,author,createdAt,state,headRefName,baseRefName",
        ],
        parse_json=True,
    )


def test_pr_manager_list_prs_empty(mock_executor: MagicMock):
    """Test PRManager.list_prs when executor returns an empty list."""
    mock_executor.execute.return_value = []

    pr_manager = PRManager(mock_executor)
    prs = pr_manager.list_prs()

    assert prs == []
    mock_executor.execute.assert_called_once_with(
        [
            "pr",
            "list",
            "--state",
            "open",
            "--limit",
            "10",
            "--json",
            "number,title,url,author,createdAt,state,headRefName,baseRefName",
        ],
        parse_json=True,
    )


def test_pr_manager_get_pr_content(mock_executor: MagicMock):
    """Test PRManager.get_pr_content with mocked executor."""
    expected_content = {
        "number": 1,
        "title": "Fix bug #123",
        "body": "This PR fixes bug #123 by ...",
        "comments": 5,
        "reviews": 2,
        "files": ["file1.py", "file2.txt"],
    }
    mock_executor.execute.return_value = expected_content

    pr_manager = PRManager(mock_executor)
    content = pr_manager.get_pr_content(number=1)

    assert content == expected_content
    mock_executor.execute.assert_called_once_with(
        ["pr", "view", "1", "--json", "number,title,body,comments,reviews,files"],
        parse_json=True,
    )


def test_pr_manager_get_pr_content_empty(mock_executor: MagicMock):
    """Test PRManager.get_pr_content when executor returns an empty dict."""
    mock_executor.execute.return_value = {}

    pr_manager = PRManager(mock_executor)
    content = pr_manager.get_pr_content(number=1)

    assert content == {}
    mock_executor.execute.assert_called_once_with(
        ["pr", "view", "1", "--json", "number,title,body,comments,reviews,files"],
        parse_json=True,
    )

def test_get_pr_diff(mock_executor: MagicMock):
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

    pr_manager = PRManager(mock_executor)
    diff = pr_manager.get_pr_diff(pr_number=456)

    expected_cmd = ["pr", "diff", "456", "--patch"]
    mock_executor.execute.assert_called_once_with(expected_cmd, parse_json=False)
    assert diff == mock_diff_output


def test_get_pr_diff_with_target_branch(mock_executor: MagicMock):
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

    pr_manager = PRManager(mock_executor)
    diff = pr_manager.get_pr_diff(pr_number=789, target_branch="main")

    expected_cmd = ["pr", "diff", "789", "--patch", "--base", "main"]
    mock_executor.execute.assert_called_once_with(expected_cmd, parse_json=False)
    assert diff == mock_diff_output


def test_pr_manager_get_pr_diff_against_branch(mock_executor: MagicMock):
    """Test PRManager.get_pr_diff_against_branch with mocked executor."""
    expected_diff = """diff --git a/file1.py b/file1.py
index abcdefg..hijklmn 100644
--- a/file1.py
+++ b/file1.py
@@ -1,3 +1,4 @@
 def my_func():
-    print("hello")
+    print("hello world from target branch")
+    # new comment
"""
    mock_executor.execute.return_value = expected_diff

    pr_manager = PRManager(mock_executor)
    diff = pr_manager.get_pr_diff_against_branch(number=1, target_branch="develop")

    assert diff == expected_diff
    mock_executor.execute.assert_called_once_with(
        ["pr", "diff", "1", "--base", "develop", "--patch"],
    )