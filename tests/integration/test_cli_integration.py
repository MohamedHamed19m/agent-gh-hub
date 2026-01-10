from typer.testing import CliRunner

from gh_wrapper.cli.main import app


def test_cli_help() -> None:
    """Verify help command works."""
    runner = CliRunner()
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    assert "scan" in result.stdout
    assert "trace" in result.stdout
    assert "analyze-branch" in result.stdout
    assert "review-pr" in result.stdout
    assert "trace-user" in result.stdout


def test_cli_scan_invalid_repo() -> None:
    """Verify error handling for invalid repo."""
    runner = CliRunner()
    # This should fail at the executor layer if repo doesn't exist
    result = runner.invoke(app, ["scan", "nonexistent/repo"])
    assert result.exit_code != 0
    # It might output to stderr or stdout depending on where it's caught
    assert "Error" in result.stdout or "Error" in result.stderr
