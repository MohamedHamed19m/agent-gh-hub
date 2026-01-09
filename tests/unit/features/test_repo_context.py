from unittest.mock import MagicMock, patch

import pytest

from gh_wrapper.core.executor import GHExecutor
from gh_wrapper.features.repo_context import RepoContextAnalyzer


@pytest.fixture
def mock_executor() -> MagicMock:
    mock = MagicMock(spec=GHExecutor)
    mock.repo = "test/repo"
    return mock


@pytest.fixture
def analyzer(mock_executor: MagicMock) -> RepoContextAnalyzer:
    return RepoContextAnalyzer(mock_executor)


def test_is_priority_file(analyzer: RepoContextAnalyzer) -> None:
    assert analyzer._is_priority_file("README.md") is True
    assert analyzer._is_priority_file("pyproject.toml") is True
    assert analyzer._is_priority_file(".github/workflows/test.yml") is True
    assert analyzer._is_priority_file("src/main.py") is False


def test_get_smart_structure_truncation(analyzer: RepoContextAnalyzer) -> None:
    # Mock repo_manager.get_file_structure
    with patch.object(analyzer.repo_manager, "get_file_structure") as mock_get:
        mock_get.return_value = [
            {"path": "README.md", "type": "file"},  # Priority
            {"path": "pyproject.toml", "type": "file"},  # Priority
            {"path": "src/a.py", "type": "file"},  # Depth 2
            {"path": "src/b.py", "type": "file"},  # Depth 2
            {"path": "src/deep/c.py", "type": "file"},  # Depth 3 (Truncated)
            {"path": "LICENSE", "type": "file"},  # Priority
        ]

        # Test with depth 2
        structure = analyzer._get_smart_structure("main", max_depth=2, max_per_level=10)

        paths = [item["path"] for item in structure]
        assert "README.md" in paths
        assert "pyproject.toml" in paths
        assert "src/a.py" in paths
        assert "src/b.py" in paths
        assert "src/deep/c.py" not in paths  # Too deep
        assert "LICENSE" in paths  # Priority even if deep (though it's depth 1)


def test_get_smart_structure_priority_preservation(
    analyzer: RepoContextAnalyzer,
) -> None:
    # Mock many files at depth 1
    files = [{"path": f"file_{i}.txt", "type": "file"} for i in range(30)]
    files.append({"path": "pyproject.toml", "type": "file"})  # Priority

    with patch.object(analyzer.repo_manager, "get_file_structure") as mock_get:
        mock_get.return_value = files

        # Limit depth 1 to 20 items
        structure = analyzer._get_smart_structure("main", max_depth=1, max_per_level=20)

        paths = [item["path"] for item in structure]
        assert "pyproject.toml" in paths  # Must be present
        assert len([p for p in paths if p.startswith("file_")]) == 20  # limited to 20
        assert any(item["type"] == "truncated" for item in structure)


def test_get_summarized_activity(analyzer: RepoContextAnalyzer) -> None:
    # Mock commits
    with (
        patch.object(
            analyzer.commits_manager, "get_commits_for_analysis"
        ) as mock_commits,
        patch.object(analyzer.pr_manager, "list_prs") as mock_prs,
    ):
        mock_commits.return_value = [
            {
                "sha": "sha123456",
                "commit": {
                    "message": "feat: test",
                    "author": {
                        "name": "User",
                        "email": "test@example.com",
                        "date": "2023-01-01",
                    },
                },
                "parents": [{}, {}],  # Merge
            }
        ]

        # Mock PRs
        mock_prs.return_value = [
            {
                "number": 1,
                "title": "PR 1",
                "author": {"login": "user1"},
                "createdAt": "2023-01-01",
                "draft": True,
            }
        ]

        activity = analyzer._get_summarized_activity("main")

        assert len(activity["recent_commits"]) == 1
        assert activity["recent_commits"][0]["sha"] == "sha1234"
        assert activity["recent_commits"][0]["is_merge"] is True

        assert len(activity["open_pull_requests"]) == 1
        assert activity["open_pull_requests"][0]["status"] == "Draft"
        assert activity["stats"]["commits_last_7d"] == 1


def test_get_readme_snippet(analyzer: RepoContextAnalyzer) -> None:
    long_content = "Line 1\n\n\n\nLine 2" + "x" * 3000
    with patch.object(analyzer.file_manager, "get_file_content") as mock_get:
        mock_get.return_value = long_content

        snippet = analyzer._get_readme_snippet("main", limit=100)

        assert snippet is not None
        assert "Line 1\n\nLine 2" in snippet
        assert "...[truncated]" in snippet
        assert len(snippet) <= 120  # approx with truncated text
