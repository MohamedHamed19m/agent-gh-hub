from unittest.mock import MagicMock

import pytest

from gh_wrapper.features.branch_analytics import BranchAnalyzer, BranchStats


@pytest.fixture
def mock_executor() -> MagicMock:
    return MagicMock()


@pytest.fixture
def analyzer(mock_executor: MagicMock) -> BranchAnalyzer:
    return BranchAnalyzer(mock_executor)


def test_branch_stats_structure() -> None:
    """Verify the Pydantic model structure."""
    stats = BranchStats(
        branch="main",
        total_commits=10,
        last_commit={"sha": "123", "author": "user", "date": "2026-01-01T00:00:00Z"},
        contributors={"user": 10},
        health_score=100.0,
    )
    assert stats.branch == "main"
    assert stats.total_commits == 10


def test_analyze_branch_logic(
    analyzer: BranchAnalyzer, mock_executor: MagicMock
) -> None:
    """Verify that analyzer calculates stats correctly from mock executor data."""
    # Mock data for list_commits
    mock_executor.execute.return_value = [
        {
            "sha": "sha1",
            "commit": {
                "author": {"name": "Alice", "date": "2026-01-02T10:00:00Z"},
                "message": "Commit 2",
            },
        },
        {
            "sha": "sha2",
            "commit": {
                "author": {"name": "Bob", "date": "2026-01-01T10:00:00Z"},
                "message": "Commit 1",
            },
        },
        {
            "sha": "sha3",
            "commit": {
                "author": {"name": "Alice", "date": "2026-01-01T09:00:00Z"},
                "message": "Initial commit",
            },
        },
    ]

    stats = analyzer.analyze_branch("main", limit=3)

    assert stats.branch == "main"
    assert stats.total_commits == 3
    assert stats.last_commit is not None
    assert stats.last_commit["sha"] == "sha1"
    assert stats.contributors["Alice"] == 2
    assert stats.contributors["Bob"] == 1
    assert stats.health_score > 0


def test_analyze_branch_empty(
    analyzer: BranchAnalyzer, mock_executor: MagicMock
) -> None:
    """Verify that analyzer handles empty commit list correctly."""
    mock_executor.execute.return_value = []

    stats = analyzer.analyze_branch("empty-branch")

    assert stats.branch == "empty-branch"
    assert stats.total_commits == 0
    assert stats.last_commit is None
