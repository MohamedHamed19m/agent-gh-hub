"""
Handler for the 'trace-user' command.
Agent B: Implementation of TOON and Rich output.
"""

import sys
from typing import Dict, List

import toon_format as toon
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from gh_wrapper.core.executor import GHExecutor
from gh_wrapper.features.user_tracer import UserTracer


def handle_trace_user(username: str, repo: str, readable: bool = False) -> None:
    """
    Execute user activity tracing and format output.
    """
    executor = GHExecutor(repo=repo)
    tracer = UserTracer(executor)

    try:
        # trace_recent_work returns List[Dict]
        activity = tracer.trace_recent_work(username, repo)

        if readable:
            render_rich_user_trace(username, repo, activity)
        else:
            # Default: TOON output
            sys.stdout.write(toon.encode(activity))
            sys.stdout.write("\n")

    except Exception as e:
        sys.stderr.write(f"Error: {str(e)}\n")
        sys.exit(1)


def render_rich_user_trace(username: str, repo: str, activity: List[Dict]) -> None:
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
            commit.get("short_name", "N/A"),
            commit.get("message", "N/A").split("\n")[0],
            commit.get("branch", "N/A"),
            commit.get("date", "N/A"),
        )

    console.print(table)
