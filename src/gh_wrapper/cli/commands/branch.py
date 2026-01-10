"""
Handler for the 'analyze-branch' command.
Agent B: Implementation of TOON and Rich output.
"""

import sys
from typing import Any

import toon_format as toon
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from gh_wrapper.core.executor import GHExecutor
from gh_wrapper.features.branch_analytics import BranchAnalyzer


def handle_analyze(repo: str, branch: str, readable: bool = False) -> None:
    """
    Execute branch analysis and format output.
    """
    executor = GHExecutor(repo=repo)
    analyzer = BranchAnalyzer(executor)

    try:
        stats = analyzer.analyze_branch(branch)

        if readable:
            render_rich_branch(stats)
        else:
            # Default: TOON output
            sys.stdout.write(toon.encode(stats.model_dump()))
            sys.stdout.write("\n")

    except Exception as e:
        sys.stderr.write(f"Error: {str(e)}\n")
        sys.exit(1)


def render_rich_branch(stats: Any) -> None:
    """
    Render branch analysis results using Rich for humans.
    """
    console = Console()

    console.print(
        Panel(f"[bold blue]Branch Analytics:[/] [green]{stats.branch}[/]", expand=False)
    )

    # Summary Table
    summary = Table(show_header=False, box=None)
    summary.add_row("Total Commits (sampled)", str(stats.total_commits))
    summary.add_row("Health Score", f"[bold]{stats.health_score}/100[/]")
    if stats.last_commit:
        summary.add_row("Last Commit SHA", stats.last_commit.get("sha", "N/A"))
        summary.add_row("Last Commit Author", stats.last_commit.get("author", "N/A"))
        summary.add_row("Last Commit Date", stats.last_commit.get("date", "N/A"))
    console.print(summary)

    # Contributors Table
    if stats.contributors:
        contrib_table = Table(title="Contributors", box=None)
        contrib_table.add_column("Author", style="cyan")
        contrib_table.add_column("Commits", justify="right")
        # Sort contributors by commit count
        sorted_contribs = sorted(
            stats.contributors.items(), key=lambda x: x[1], reverse=True
        )
        for author, count in sorted_contribs:
            contrib_table.add_row(author, str(count))
        console.print(contrib_table)
