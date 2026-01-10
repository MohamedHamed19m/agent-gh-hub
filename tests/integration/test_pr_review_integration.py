import os

import pytest

from gh_wrapper.commands.pull_requests import PRManager
from gh_wrapper.core.executor import GHExecutor
from gh_wrapper.features.pr_review_analyzer import PrReviewAnalyzer
from gh_wrapper.models.pr_review import PrReviewInput, PrReviewOutput


@pytest.mark.integration
def test_pr_review_integration_real_repo() -> None:
    """
    Integration test using the current repository.
    Requires GH_TOKEN and gh CLI to be authenticated.
    """
    if not os.getenv("RUN_INTEGRATION_TESTS") and not os.getenv("GITHUB_ACTIONS"):
        pytest.skip("Skipping integration test. Set RUN_INTEGRATION_TESTS=1 to run.")

    executor = GHExecutor()
    pr_manager = PRManager(executor)
    analyzer = PrReviewAnalyzer(pr_manager)

    # List open PRs to find one to test against
    prs = pr_manager.list_prs(state="all", limit=1)
    if not prs:
        pytest.skip("No PRs found in the current repository to test against.")

    pr_id = prs[0]["number"]

    # We don't have owner/repo easily available here without parsing,
    # but analyze_pr doesn't strictly use it for logic, only for title.
    # The executor handles the actual repo context.
    pr_input = PrReviewInput(repo_name="this-repo", pr_id=pr_id, review_depth="full")

    report = analyzer.analyze_pr(pr_input)

    assert isinstance(report, PrReviewOutput)
    assert report.input_params.pr_id == pr_id
    assert "lines_added" in report.metrics
    assert "files_changed" in report.metrics

    # Verify Markdown formatting
    markdown = analyzer.format_as_markdown(report)
    assert "# PR Review for this-repo#" in markdown
    assert "## Summary" in markdown
    assert "## Metrics" in markdown
