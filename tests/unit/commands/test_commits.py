import json
from typing import Any, Dict

from gh_wrapper.commands.commits import CommitsManager


def test_list_commits(
    mock_executor: Any, sample_commit_response: Dict[str, Any]
) -> None:
    executor, mock_run = mock_executor
    # reset mock to ignore init calls
    mock_run.reset_mock()

    mock_run.return_value.stdout = json.dumps([sample_commit_response])

    manager = CommitsManager(executor)
    commits = manager.list_commits(branch="main", limit=5)

    assert len(commits) > 0
    assert commits[0]["sha"] == "abc123456789"

    # Verify arguments
    args, _ = mock_run.call_args
    # args[0] is the command list
    cmd = args[0]
    assert cmd[0] == "gh"
    assert "api" in cmd
    # We expect repos/test/repo/commits because executor.repo is set
    assert any("repos/test/repo/commits" in str(arg) for arg in cmd)


def test_search_commits(mock_executor: Any) -> None:
    executor, mock_run = mock_executor
    mock_run.reset_mock()

    mock_run.return_value.stdout = json.dumps({"items": [{"sha": "search_result"}]})

    manager = CommitsManager(executor)
    results = manager.search_commits("bugfix")

    assert len(results) == 1
    assert results[0]["sha"] == "search_result"


def test_get_commits_for_analysis(
    mock_executor: Any, sample_commit_response: Dict[str, Any]
) -> None:
    executor, mock_run = mock_executor
    mock_run.reset_mock()

    mock_run.return_value.stdout = json.dumps([sample_commit_response])

    manager = CommitsManager(executor)
    commits = manager.get_commits_for_analysis(branch="develop", since="2023-01-01")

    assert len(commits) == 1
    assert commits[0]["sha"] == "abc123456789"
    # Full response should have "commit" key
    assert "commit" in commits[0]

    args, _ = mock_run.call_args
    cmd = args[0]
    assert any("sha=develop" in str(arg) for arg in cmd)
    assert any("since=2023-01-01" in str(arg) for arg in cmd)
