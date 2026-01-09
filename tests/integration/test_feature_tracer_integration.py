import os

import pytest

from gh_wrapper.features.feature_tracer import FeatureTracer
from gh_wrapper.models.trace import MultiRepoFeatureTrace


@pytest.mark.integration
def test_feature_tracer_integration_real_repo() -> None:
    """
    Integration test using a real public repository.
    Requires GH_TOKEN and gh CLI to be authenticated.
    """
    if not os.getenv("RUN_INTEGRATION_TESTS") and not os.getenv("GITHUB_ACTIONS"):
        pytest.skip("Skipping integration test. Set RUN_INTEGRATION_TESTS=1 to run.")

    tracer = FeatureTracer()

    # Trace a common keyword in cli/cli
    report = tracer.trace_feature(
        keyword="release",
        repos=["cli/cli"],
        branches=["trunk"],
        max_commits_per_branch=50,
    )

    assert isinstance(report, MultiRepoFeatureTrace)
    assert report.keyword == "release"
    assert "cli/cli" in report.traces

    trace = report.traces["cli/cli"]
    assert trace.total_mentions > 0

    markdown = tracer.format_as_markdown(report)
    assert "# Feature Trace Report: release" in markdown
    assert "cli/cli" in markdown
