"""
Handler for the 'trace' command.
Agent B: Implementation of TOON and Rich output.
"""

import os
import sys
from typing import Any, Optional

import typer
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from toon import encode as toon_encode

from gh_wrapper.features.feature_tracer import FeatureTracer


def handle_trace(
    query: str, repos_str: Optional[str] = None, readable: bool = False
) -> None:
    """
    Execute feature tracing and format output.
    """
    if repos_str:
        repos = [r.strip() for r in repos_str.split(",")]
    else:
        # Fallback to GH_REPO or similar if available, or error
        repo = os.environ.get("GH_REPO")
        if not repo:
            sys.stderr.write(
                "Error: No repositories specified. "
                "Use --repos or set GH_REPO env var.\n"
            )
            sys.exit(1)
        repos = [repo]

    tracer = FeatureTracer()

    try:
        report = tracer.trace_feature(query, repos=repos)

        if readable:
            render_rich_trace(report)
        else:
            # Default: TOON output
            typer.echo(toon_encode(report.model_dump()))

    except Exception as e:
        sys.stderr.write(f"Error: {str(e)}\n")
        sys.exit(1)


def render_rich_trace(report: Any) -> None:
    """
    Render trace results using Rich for humans.
    """
    console = Console()

    console.print(
        Panel(
            f"[bold blue]Feature Trace Report:[/] [yellow]{report.keyword}[/]",
            expand=False,
        )
    )

    for repo_name, trace in report.traces.items():
        console.rule(f"[bold green]Repository: {repo_name}[/]")

        # Summary Table
        summary = Table(show_header=False, box=None)
        summary.add_row("Total Mentions", str(trace.total_mentions))
        summary.add_row("File Matches", str(len(trace.file_matches)))
        summary.add_row("Commit Matches", str(len(trace.commit_matches)))
        summary.add_row("PR Matches", str(len(trace.pr_matches)))
        console.print(summary)

        # Contributors
        if trace.contributors:
            contrib_table = Table(title="Top Contributors", box=None)
            contrib_table.add_column("Username", style="cyan")
            contrib_table.add_column("Commits", justify="right")
            contrib_table.add_column("PRs", justify="right")
            for c in trace.contributors[:5]:
                contrib_table.add_row(
                    c["username"], str(c["commit_count"]), str(c["pr_count"])
                )
            console.print(contrib_table)

        # File Matches
        if trace.file_matches:
            file_table = Table(title="File Matches", box=None)
            file_table.add_column("Path", style="magenta")
            for f in trace.file_matches[:10]:
                file_table.add_row(f.path)
            console.print(file_table)

        # Commit Matches
        if trace.commit_matches:
            commit_table = Table(title="Recent Commit Matches", box=None)
            commit_table.add_column("SHA", style="dim")
            commit_table.add_column("Message", style="white")
            commit_table.add_column("Author", style="cyan")
            commit_table.add_column("Date", style="magenta")
            for c in trace.commit_matches[:10]:
                msg = c.message.split("\n")[0]
                commit_table.add_row(
                    c.sha[:7],
                    msg[:50] + "..." if len(msg) > 50 else msg,
                    c.author,
                    c.date[:10],
                )
            console.print(commit_table)

        # PR Matches
        if trace.pr_matches:
            pr_table = Table(title="PR Matches", box=None)
            pr_table.add_column("ID", style="dim")
            pr_table.add_column("Title", style="white")
            pr_table.add_column("Status", style="green")
            for p in trace.pr_matches[:10]:
                pr_table.add_row(
                    f"#{p.number}",
                    p.title,
                    p.status,
                )
            console.print(pr_table)

        console.print("\n")
