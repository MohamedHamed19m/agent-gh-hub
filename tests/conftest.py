from unittest.mock import patch

import pytest

from gh_wrapper.core.executor import GHExecutor


@pytest.fixture
def mock_executor():
    """Mock executor for testing without actual gh calls"""
    with patch("subprocess.run") as mock_run:
        # Default mock response
        mock_run.return_value.stdout = '{"test": "data"}'
        mock_run.return_value.returncode = 0

        # We also need to mock the version check in __init__
        # But since we patch subprocess.run, it handles it.
        # However, the __init__ calls it immediately.
        # So we might need to be careful.
        # Actually, since we patch subprocess.run *before* creating GHExecutor, it should capture the version check too.

        executor = GHExecutor(repo="test/repo")
        yield executor, mock_run


@pytest.fixture
def sample_commit_response():
    return {
        "sha": "abc123456789",
        "commit": {"message": "Test commit", "author": {"name": "Test User"}},
    }
