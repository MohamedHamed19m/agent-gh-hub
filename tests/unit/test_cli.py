from unittest.mock import MagicMock, patch


def test_cli_initialization() -> None:
    """
    Verify the CLI app is correctly initialized.
    """
    from gh_wrapper.cli.main import app

    assert app is not None


def test_cli_commands_registered() -> None:
    """
    Verify that all required commands are registered in the Typer app.
    """
    from gh_wrapper.cli.main import app

    # In Typer, name is None if not explicitly provided, defaults to function name
    command_names = [
        cmd.name or cmd.callback.__name__.replace("_", "-")
        for cmd in app.registered_commands
    ]
    expected_commands = [
        "scan",
        "trace",
        "analyze-branch",
        "review-pr",
        "trace-user",
    ]
    for cmd in expected_commands:
        assert cmd in command_names


@patch("gh_wrapper.cli.commands.scan.handle_scan")
def test_scan_command_delegation(mock_handle: MagicMock) -> None:
    """
    Verify scan command delegates to its handler.
    """
    from typer.testing import CliRunner

    from gh_wrapper.cli.main import app

    runner = CliRunner()
    result = runner.invoke(app, ["scan", "owner/repo"])
    assert result.exit_code == 0
    mock_handle.assert_called_once_with("owner/repo", None, False)


@patch("gh_wrapper.cli.commands.trace.handle_trace")
def test_trace_command_delegation(mock_handle: MagicMock) -> None:
    """
    Verify trace command delegates to its handler.
    """
    from typer.testing import CliRunner

    from gh_wrapper.cli.main import app

    runner = CliRunner()
    result = runner.invoke(app, ["trace", "query", "--repos", "r1,r2"])
    assert result.exit_code == 0
    mock_handle.assert_called_once_with("query", "r1,r2", False)


@patch("gh_wrapper.cli.commands.branch.handle_analyze")
def test_analyze_branch_command_delegation(mock_handle: MagicMock) -> None:
    """
    Verify analyze-branch command delegates to its handler.
    """
    from typer.testing import CliRunner

    from gh_wrapper.cli.main import app

    runner = CliRunner()
    result = runner.invoke(app, ["analyze-branch", "owner/repo", "main"])
    assert result.exit_code == 0
    mock_handle.assert_called_once_with("owner/repo", "main", False)


@patch("gh_wrapper.cli.commands.pr.handle_review")
def test_review_pr_command_delegation(mock_handle: MagicMock) -> None:
    """
    Verify review-pr command delegates to its handler.
    """
    from typer.testing import CliRunner

    from gh_wrapper.cli.main import app

    runner = CliRunner()
    result = runner.invoke(app, ["review-pr", "owner/repo", "123"])
    assert result.exit_code == 0
    mock_handle.assert_called_once_with("owner/repo", 123, False)


@patch("gh_wrapper.cli.commands.user.handle_trace_user")
def test_trace_user_command_delegation(mock_handle: MagicMock) -> None:
    """
    Verify trace-user command delegates to its handler.
    """
    from typer.testing import CliRunner

    from gh_wrapper.cli.main import app

    runner = CliRunner()
    result = runner.invoke(app, ["trace-user", "username", "--repo", "owner/repo"])
    assert result.exit_code == 0
    mock_handle.assert_called_once_with("username", "owner/repo", False)
