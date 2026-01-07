import subprocess
from typing import Generator
from unittest.mock import MagicMock, patch

import pytest

from gh_wrapper.core.exceptions import GHCommandError, GHNotInstalledError
from gh_wrapper.core.executor import GHExecutor


@pytest.fixture
def mock_subprocess_run() -> Generator[MagicMock, None, None]:
    with patch("subprocess.run") as mock:
        # Mock version check
        mock.return_value = MagicMock(stdout="gh version 2.0.0", returncode=0)
        yield mock


def test_executor_init_checks_gh(mock_subprocess_run: MagicMock) -> None:
    GHExecutor()
    mock_subprocess_run.assert_called_with(
        ["gh", "--version"], capture_output=True, check=True, timeout=5
    )


def test_executor_gh_not_installed() -> None:
    with patch("subprocess.run", side_effect=FileNotFoundError):
        with pytest.raises(GHNotInstalledError):
            GHExecutor()


def test_executor_execute_basic(mock_subprocess_run: MagicMock) -> None:
    executor = GHExecutor(repo="owner/repo")
    mock_subprocess_run.return_value = MagicMock(stdout="output", returncode=0)

    result = executor.execute(["auth", "status"])

    assert result == "output"
    # Verify --repo was added
    last_call_args = mock_subprocess_run.call_args[0][0]
    assert "--repo" in last_call_args
    assert "owner/repo" in last_call_args


def test_executor_execute_json(mock_subprocess_run: MagicMock) -> None:
    executor = GHExecutor()
    mock_subprocess_run.return_value = MagicMock(
        stdout='{"key": "value"}', returncode=0
    )

    result = executor.execute(["pr", "list"], parse_json=True)

    assert result == {"key": "value"}


def test_executor_repo_formatting(mock_subprocess_run: MagicMock) -> None:
    with patch.dict(
        "os.environ", {"GH_HOST": "github.enterprise.com", "GH_ORG": "myorg"}
    ):
        executor = GHExecutor(repo="myrepo")
        mock_subprocess_run.return_value = MagicMock(stdout="ok", returncode=0)
        executor.execute(["status"])

        last_call_args = mock_subprocess_run.call_args[0][0]
        assert "github.enterprise.com/myorg/myrepo" in last_call_args


def test_executor_caching(mock_subprocess_run: MagicMock) -> None:
    executor = GHExecutor(use_cache=True)
    mock_subprocess_run.return_value = MagicMock(stdout="first", returncode=0)

    # First call
    res1 = executor.execute(["status"])
    assert res1 == "first"
    assert mock_subprocess_run.call_count == 2  # 1 for init, 1 for execute

    # Second call (cached)
    res2 = executor.execute(["status"])
    assert res2 == "first"
    assert mock_subprocess_run.call_count == 2


def test_executor_error_handling(mock_subprocess_run: MagicMock) -> None:
    # Setup side effect for the next TWO calls to subprocess.run
    # 1. Inside GHExecutor() constructor (_verify_gh_installed)
    # 2. Inside executor.execute(...)
    mock_subprocess_run.side_effect = [
        MagicMock(stdout="gh version 2.0.0", returncode=0),
        subprocess.CalledProcessError(1, "gh", stderr="error message"),
    ]

    executor = GHExecutor()

    with pytest.raises(GHCommandError) as excinfo:
        executor.execute(["invalid"])
    assert "error message" in str(excinfo.value)
