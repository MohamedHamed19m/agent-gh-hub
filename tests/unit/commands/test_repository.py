import json
from typing import Any, Dict, List
from unittest.mock import patch

from gh_wrapper.commands.repository import RepoManager


def test_list_branches(mock_executor: Any) -> None:
    executor, mock_run = mock_executor
    mock_run.reset_mock()

    mock_run.return_value.stdout = json.dumps([{"name": "main"}, {"name": "develop"}])

    manager = RepoManager(executor)
    branches = manager.list_branches(limit=2)

    assert len(branches) == 2
    assert branches[0]["name"] == "main"
    full_cmd = " ".join(map(str, mock_run.call_args[0][0]))
    assert "repos/test/repo/branches" in full_cmd


def test_get_repo_basics(mock_executor: Any) -> None:
    executor, mock_run = mock_executor
    mock_run.reset_mock()

    mock_run.return_value.stdout = json.dumps(
        {
            "defaultBranchRef": {"name": "main"},
            "description": "Test repo",
            "latestRelease": {"tagName": "v1.0.0"},
        }
    )

    manager = RepoManager(executor)
    basics = manager.get_repo_basics()

    assert basics["default_branch"] == "main"
    assert basics["description"] == "Test repo"
    assert basics["latest_release"] == "v1.0.0"


def test_get_file_structure(mock_executor: Any) -> None:
    executor, mock_run = mock_executor
    mock_run.reset_mock()

    mock_run.return_value.stdout = json.dumps(
        {
            "tree": [
                {"path": "src", "type": "tree", "sha": "s1"},
                {"path": "README.md", "type": "blob", "sha": "s2"},
            ]
        }
    )

    manager = RepoManager(executor)
    structure = manager.get_file_structure("main")

    assert len(structure) == 2
    assert structure[0]["type"] == "dir"
    assert structure[1]["type"] == "file"


def test_get_recent_commits(mock_executor: Any) -> None:
    executor, mock_run = mock_executor
    mock_run.reset_mock()

    mock_run.return_value.stdout = json.dumps(
        [
            {
                "sha": "abcdef123456",
                "commit": {
                    "message": "Fix bug\n\nDetailed desc",
                    "author": {"name": "Author", "date": "2023-01-01"},
                },
            }
        ]
    )

    manager = RepoManager(executor)
    commits = manager.get_recent_commits("main", limit=1)

    assert len(commits) == 1
    assert commits[0]["sha"] == "abcdef1"
    assert commits[0]["message"] == "Fix bug"


def test_get_priority_branches_threaded(mock_executor: Any) -> None:
    executor, mock_run = mock_executor
    mock_run.reset_mock()

    with patch.object(executor, "execute") as mock_execute:

        def mock_execute_side_effect(
            cmd: List[Any], parse_json: bool = True
        ) -> Dict[str, Any]:
            cmd_str = " ".join(map(str, cmd))
            if "branches/main" in cmd_str:
                return {"name": "main", "commit": {"sha": "sha_main"}}
            if "branches/develop" in cmd_str:
                return {"name": "develop", "commit": {"sha": "sha_dev"}}
            if "branches/missing" in cmd_str:
                return {"_error": "Not Found"}
            return {}

        mock_execute.side_effect = mock_execute_side_effect

        manager = RepoManager(executor, max_concurrent=2)
        priority_branches = manager.get_priority_branches(
            ["main", "develop", "missing"]
        )

        assert len(priority_branches) == 2
        names = [b["name"] for b in priority_branches]
        assert "main" in names
        assert "develop" in names
        assert "missing" not in names


def test_get_latest_branches_graphql(mock_executor: Any) -> None:
    executor, mock_run = mock_executor
    mock_run.reset_mock()

    mock_run.return_value.stdout = json.dumps(
        {
            "data": {
                "repository": {
                    "refs": {
                        "nodes": [
                            {
                                "name": "feat/1",
                                "target": {
                                    "oid": "sha1",
                                    "committedDate": "2023-01-01",
                                },
                            }
                        ]
                    }
                }
            }
        }
    )

    manager = RepoManager(executor)
    branches = manager.get_latest_branches_graphql(scan_limit=1)

    assert len(branches) == 1
    assert branches[0]["name"] == "feat/1"


def test_get_combined_branches(mock_executor: Any) -> None:
    executor, mock_run = mock_executor
    mock_run.reset_mock()

    manager = RepoManager(executor)

    with (
        patch.object(manager, "get_priority_branches") as mock_priority,
        patch.object(manager, "get_latest_branches_graphql") as mock_latest,
    ):
        mock_priority.return_value = [{"name": "main", "sha": "s1"}]
        mock_latest.return_value = [
            {"name": "main", "sha": "s1"},
            {"name": "feat/1", "sha": "s2"},
        ]

        combined = manager.get_combined_branches(scan_limit=50)

        assert len(combined) == 2
        names = [b["name"] for b in combined]
        assert "main" in names
        assert "feat/1" in names


def test_get_default_branch(mock_executor: Any) -> None:
    executor, mock_run = mock_executor
    mock_run.reset_mock()

    manager = RepoManager(executor)
    with patch.object(manager, "get_repo_basics") as mock_basics:
        mock_basics.return_value = {"default_branch": "develop"}
        assert manager.get_default_branch() == "develop"
