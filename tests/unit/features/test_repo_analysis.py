from unittest.mock import MagicMock

import pytest

from gh_wrapper.commands.commits import CommitsManager
from gh_wrapper.features.repo_analysis import RepoAnalyzer
from gh_wrapper.models.analysis import (
    CommitAnalysisReport,
    ContributorStats,
    DailyStats,
    TimePatterns,
)


@pytest.fixture
def mock_executor() -> MagicMock:
    mock = MagicMock()
    mock.repo = "test/repo"
    return mock


@pytest.fixture
def mock_commits_manager(mock_executor: MagicMock) -> MagicMock:
    manager = MagicMock(spec=CommitsManager)
    manager.executor = mock_executor
    return manager


@pytest.fixture
def repo_analyzer(mock_commits_manager: MagicMock) -> RepoAnalyzer:
    return RepoAnalyzer(mock_commits_manager)


def test_analyze_commit_patterns_basic(
    repo_analyzer: RepoAnalyzer, mock_commits_manager: MagicMock
) -> None:
    # Mock data
    mock_commits = [
        {
            "sha": "sha1",
            "commit": {"author": {"name": "User 1", "date": "2023-01-01T10:00:00Z"}},
        },
        {
            "sha": "sha2",
            "commit": {"author": {"name": "User 2", "date": "2023-01-01T11:00:00Z"}},
        },
        {
            "sha": "sha3",
            "commit": {"author": {"name": "User 1", "date": "2023-01-02T10:00:00Z"}},
        },
    ]

    mock_commits_manager.get_commits_for_analysis.return_value = mock_commits

    report = repo_analyzer.analyze_commit_patterns(branches=["main"], days_back=30)

    assert isinstance(report, CommitAnalysisReport)
    assert report.total_commits == 3
    assert len(report.contributors) == 2
    # Authors are sorted by count
    assert report.contributors[0].author == "User 1"
    assert report.contributors[0].commit_count == 2
    assert report.contributors[0].percentage == pytest.approx(66.67, rel=1e-2)

    assert len(report.daily_trends) == 2
    assert report.daily_trends[0].date == "2023-01-01"
    assert report.daily_trends[0].commit_count == 2

    assert report.time_patterns.hourly_distribution[10] == 2
    assert report.time_patterns.hourly_distribution[11] == 1
    # Check weekday (2023-01-01 was Sunday, 2023-01-02 was Monday)
    assert report.time_patterns.weekday_distribution["Sunday"] == 2
    assert report.time_patterns.weekday_distribution["Monday"] == 1


def test_analyze_commit_patterns_invalid_inputs(repo_analyzer: RepoAnalyzer) -> None:
    with pytest.raises(ValueError, match="At least one branch must be provided"):
        repo_analyzer.analyze_commit_patterns(branches=[], days_back=30)

    with pytest.raises(ValueError, match="days_back must be a positive integer"):
        repo_analyzer.analyze_commit_patterns(branches=["main"], days_back=0)


def test_analyze_commit_patterns_empty_history(
    repo_analyzer: RepoAnalyzer, mock_commits_manager: MagicMock
) -> None:
    mock_commits_manager.get_commits_for_analysis.return_value = []

    report = repo_analyzer.analyze_commit_patterns(branches=["main"], days_back=30)

    assert report.total_commits == 0
    assert len(report.daily_trends) == 0
    assert len(report.contributors) == 0
    assert all(
        count == 0 for count in report.time_patterns.hourly_distribution.values()
    )


def test_analyze_commit_patterns_api_failure(
    repo_analyzer: RepoAnalyzer, mock_commits_manager: MagicMock
) -> None:
    mock_commits_manager.get_commits_for_analysis.side_effect = Exception("API Error")

    # Should not raise exception but log warning and return empty/partial report
    report = repo_analyzer.analyze_commit_patterns(branches=["main"], days_back=30)

    assert report.total_commits == 0


def test_format_as_markdown(repo_analyzer: RepoAnalyzer) -> None:
    report = CommitAnalysisReport(
        repository="test/repo",
        branches=["main"],
        since="2023-01-01T00:00:00Z",
        total_commits=10,
        daily_trends=[DailyStats(date="2023-01-01", commit_count=10)],
        contributors=[
            ContributorStats(author="User 1", commit_count=10, percentage=100.0)
        ],
        time_patterns=TimePatterns(
            hourly_distribution={i: (10 if i == 12 else 0) for i in range(24)},
            weekday_distribution={
                d: (10 if d == "Monday" else 0)
                for d in [
                    "Monday",
                    "Tuesday",
                    "Wednesday",
                    "Thursday",
                    "Friday",
                    "Saturday",
                    "Sunday",
                ]
            },
        ),
    )

    markdown = repo_analyzer.format_as_markdown(report)

    assert "# Repository Analysis Report" in markdown
    assert "test/repo" in markdown
    assert "User 1" in markdown
    assert "100.0%" in markdown
    assert "2023-01-01" in markdown
