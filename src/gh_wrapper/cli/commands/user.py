"""
Handler for the 'trace-user' command.
Agent B: Implementation of TOON and Rich output.
"""

import sys
from typing import List

import typer
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from toon import encode as toon_encode

from gh_wrapper.core.executor import GHExecutor
from gh_wrapper.features.user_tracer import UserTracer
from gh_wrapper.models.trace import TraceCommit


def handle_trace_user(username: str, repo: str, readable: bool = False) -> None:
    """
    Execute user activity tracing and format output.
    """
    executor = GHExecutor(repo=repo)
    tracer = UserTracer(executor)

    try:
        # trace_recent_work returns List[TraceCommit]
        activity = tracer.trace_recent_work(username, repo)

        if readable:
            render_rich_user_trace(username, repo, activity)
        else:
            # Default: TOON output
            # Convert list of models to list of dicts for encoding
            data = [c.model_dump() for c in activity]
            typer.echo(toon_encode(data))

    except Exception as e:
        sys.stderr.write(f"Error: {str(e)}\n")
        sys.exit(1)


def render_rich_user_trace(username: str, repo: str, activity: List[TraceCommit]) -> None:
    """
    Render user activity results using Rich for humans.
    """
    console = Console()

    console.print(
        Panel(
            f"[bold blue]User Activity Trace:[/ ] "
            f"[yellow]{username}[/] in [green]{repo}[/]",
            expand=False,
        )
    )

    if not activity:
        console.print(
            "[dim]No recent activity found for this user in the "
            "specified repository.[/]"
        )
        return

    table = Table(title=f"Recent Commits by {username}", box=None)
    table.add_column("SHA", style="dim")
    table.add_column("Message", style="white")
    table.add_column("Branch", style="cyan")
    table.add_column("Date", style="magenta")

    for commit in activity:
        table.add_row(
            commit.sha[:7],
            commit.message.split("\n")[0],
            commit.branch,
            commit.date[:10],
        )

    console.print(table)
