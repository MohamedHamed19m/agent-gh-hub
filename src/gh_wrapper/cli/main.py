"""CLI Implementation using Typer.
Agent B: Implementation of infrastructure and commands.
"""

from typing import Annotated

import typer

from gh_wrapper.utils.cli_helpers import toon_unsupported

app = typer.Typer(
    name="gh-bridge",
    help="Pythonic wrapper around GitHub CLI optimized for AI agents.",
    no_args_is_help=True,
    add_completion=False,
)


@app.command()
def scan(
    repo: Annotated[str, typer.Argument(help="Repository name (owner/repo)")],
    branch: Annotated[str | None, typer.Option(help="Branch name")] = None,
    readable: Annotated[
        bool, typer.Option("--readable", help="Human-readable output")
    ] = False,
) -> None:
    """Repository context analysis."""
    # Agent B: Implementation for Phase 2
    from gh_wrapper.cli.commands.scan import handle_scan

    handle_scan(repo, branch, readable)


@app.command()
def trace(
    query: Annotated[str, typer.Argument(help="Feature/code search query")],
    repos: Annotated[
        str | None, typer.Option(help="Comma-separated repository names")
    ] = None,
    readable: Annotated[
        bool, typer.Option("--readable", help="Human-readable output")
    ] = False,
) -> None:
    """Feature/code tracing."""
    # Agent B: Implementation for Phase 2
    from gh_wrapper.cli.commands.trace import handle_trace

    handle_trace(query, repos, readable)


@app.command()
def analyze_branch(
    repo: Annotated[str, typer.Argument(help="Repository name (owner/repo)")],
    branch: Annotated[str, typer.Argument(help="Branch name")],
    readable: Annotated[
        bool, typer.Option("--readable", help="Human-readable output")
    ] = False,
) -> None:
    """Branch analytics."""
    # Agent B: Implementation for Phase 2
    from gh_wrapper.cli.commands.branch import handle_analyze

    handle_analyze(repo, branch, readable)


@app.command()
@toon_unsupported
def review_pr(
    repo: Annotated[str, typer.Argument(help="Repository name (owner/repo)")],
    pr_id: Annotated[int, typer.Argument(help="Pull Request ID")],
    readable: Annotated[
        bool, typer.Option("--readable", help="Human-readable output")
    ] = False,
) -> None:
    """PR review analysis."""
    # Agent B: Implementation for Phase 3
    from gh_wrapper.cli.commands.pr import handle_review

    handle_review(repo, pr_id, readable)


@app.command()
def trace_user(
    username: Annotated[str, typer.Argument(help="GitHub username")],
    repo: Annotated[str, typer.Option(help="Repository to trace activity in")],
    readable: Annotated[
        bool, typer.Option("--readable", help="Human-readable output")
    ] = False,
) -> None:
    """User activity tracking."""
    # Agent B: Implementation for Phase 2
    from gh_wrapper.cli.commands.user import handle_trace_user

    handle_trace_user(username, repo, readable)
