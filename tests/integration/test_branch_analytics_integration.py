import os
import pytest
from gh_wrapper.core.executor import GHExecutor
from gh_wrapper.features.branch_analytics import BranchAnalyzer

@pytest.mark.integration
def test_branch_analytics_integration_real_repo():
    """
    Integration test using a real public repository.
    Requires GH_TOKEN and gh CLI to be authenticated.
    """
    if not os.getenv("RUN_INTEGRATION_TESTS") and not os.getenv("GITHUB_ACTIONS"):
        pytest.skip("Skipping integration test. Set RUN_INTEGRATION_TESTS=1 to run.")

    # Use a well-known public repository
    executor = GHExecutor(repo="cli/cli")
    analyzer = BranchAnalyzer(executor)
    
    # Analyze the main branch
    stats = analyzer.analyze_branch("trunk", limit=10)
    
    assert stats.branch == "trunk"
    assert stats.total_commits > 0
    assert stats.last_commit is not None
    assert "sha" in stats.last_commit
    assert "author" in stats.last_commit
    assert len(stats.contributors) > 0
    assert stats.health_score > 0
