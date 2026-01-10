"""Handler for the 'scan' command.
Agent B: Implementation of TOON and Rich output.
"""

import sys

import typer
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.tree import Tree
from toon import encode as toon_encode

from gh_wrapper.core.executor import GHExecutor
from gh_wrapper.features.repo_context import RepoContextAnalyzer
from gh_wrapper.models.analysis import RepoContextReport


def handle_scan(repo: str, branch: str | None = None, readable: bool = False) -> None:
    """Execute repository scanning and format output."""
    executor = GHExecutor(repo=repo)
    analyzer = RepoContextAnalyzer(executor)

    try:
        report = analyzer.analyze_current_context(branch=branch)

        if readable:
            render_rich_scan(report)
        else:
            # Default: TOON output for agents
            typer.echo(toon_encode(report.model_dump()))

    except Exception as e:
        # User-facing errors must output plain text to stderr
        sys.stderr.write(f"Error: {str(e)}\n")
        sys.exit(1)


def render_rich_scan(report: RepoContextReport) -> None:
    """Render scan results using Rich for humans."""
    console = Console()

    # Header
    console.print(
        Panel(
            f"[bold blue]Repository Scan:[/] [green]{report.target}[/]\n",
            expand=False,
        )
    )

    # Metadata Table
    meta_table = Table(title="Repository Metadata", show_header=False, box=None)
    meta = report.metadata
    meta_table.add_row("Default Branch", meta.default_branch)
    meta_table.add_row("Description", meta.description or "N/A")
    meta_table.add_row("Stars", str(meta.stars))
    meta_table.add_row("Topics", ", ".join(meta.topics))
    console.print(meta_table)

    # Structure Tree
    tree = Tree(f"[bold cyan]{report.target}[/]")
    for item in report.structure:
        if item.type == "truncated":
            tree.add(
                f"[dim]... {item.count} more items at depth "
                f"{item.path.split('_')[1]}[/]'"
            )
        else:
            icon = "📁" if item.type == "directory" else "📄"
            tree.add(f"{icon} {item.path}")
    console.print(Panel(tree, title="File Structure", border_style="cyan"))

    # Activity Stats
    stats = report.activity.stats
    stats_table = Table(title="Recent Activity (Last 7 Days)", box=None)
    stats_table.add_column("Stat", style="bold")
    stats_table.add_column("Value", style="green")
    stats_table.add_row("Commits", str(stats.commits_last_7d))
    stats_table.add_row("Open PRs", str(stats.open_prs_count))
    stats_table.add_row("Active Contributors", str(stats.active_contributors_last_7d))
    console.print(stats_table)
