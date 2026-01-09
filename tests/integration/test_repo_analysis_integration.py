import os

import pytest

from gh_wrapper.commands.commits import CommitsManager
from gh_wrapper.core.executor import GHExecutor
from gh_wrapper.features.repo_analysis import RepoAnalyzer
from gh_wrapper.models.analysis import CommitAnalysisReport


@pytest.mark.integration
def test_repo_analysis_integration_real_repo() -> None:
    """
    Integration test using the current repository and test-branch-fixture.
    Requires GH_TOKEN and gh CLI to be authenticated.
    """
    if not os.getenv("RUN_INTEGRATION_TESTS") and not os.getenv("GITHUB_ACTIONS"):
        pytest.skip("Skipping integration test. Set RUN_INTEGRATION_TESTS=1 to run.")

    # Use the current repo (assuming it's gh-bridge or agent-gh-hub)
    # The executor will resolve :owner/:repo
    executor = GHExecutor()
    commits_manager = CommitsManager(executor)
    analyzer = RepoAnalyzer(commits_manager)

    # Analyze multiple branches including the fixture
    branches = ["main", "test-branch-fixture"]
    report = analyzer.analyze_commit_patterns(branches=branches, days_back=90)

    assert isinstance(report, CommitAnalysisReport)
    assert report.total_commits > 0
    assert len(report.contributors) > 0

    # Check for specific branch presence in report metadata
    for branch in branches:
        assert branch in report.branches

    # Verify Markdown formatting
    markdown = analyzer.format_as_markdown(report)
    assert "# Repository Analysis Report" in markdown
    assert "Contributor Activity" in markdown
    assert "Daily Trends" in markdown

    # Ensure some data is actually captured in the tables
    assert "|" in markdown
