"""
Handler for the 'scan' command.
Agent B: Implementation of TOON and Rich output.
"""

import sys
from typing import Any, Dict, Optional

import toon_format as toon
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.tree import Tree

from gh_wrapper.core.executor import GHExecutor
from gh_wrapper.features.repo_context import RepoContextAnalyzer


def handle_scan(
    repo: str, branch: Optional[str] = None, readable: bool = False
) -> None:
    """
    Execute repository scanning and format output.
    """
    executor = GHExecutor(repo=repo)
    analyzer = RepoContextAnalyzer(executor)

    try:
        data = analyzer.analyze_current_context(branch=branch)

        if readable:
            render_rich_scan(data)
        else:
            # Default: TOON output
            sys.stdout.write(toon.encode(data))
            sys.stdout.write("\n")

    except Exception as e:
        # User-facing errors must output plain text to stderr
        sys.stderr.write(f"Error: {str(e)}\n")
        sys.exit(1)


def render_rich_scan(data: Dict[str, Any]) -> None:
    """
    Render scan results using Rich for humans.
    """
    console = Console()

    # Header
    console.print(
        Panel(
            f"[bold blue]Repository Scan:[/] [green]{data['target']}[/]\n"
            f"[dim]Generated at: {data['metadata'].get('fetched_at', 'N/A')}[/",
            expand=False,
        )
    )

    # Metadata Table
    meta_table = Table(title="Repository Metadata", show_header=False, box=None)
    meta = data["metadata"]
    meta_table.add_row("Name", meta.get("full_name"))
    meta_table.add_row("Default Branch", meta.get("default_branch"))
    meta_table.add_row("Stars", str(meta.get("stargazers_count")))
    meta_table.add_row("Topics", ", ".join(meta.get("topics", [])))
    console.print(meta_table)

    # Structure Tree
    tree = Tree(f"[bold cyan]{data['target']}[/]")
    for item in data["structure"]:
        if item.get("type") == "truncated":
            tree.add(
                f"[dim]... {item['count']} more items at depth "
                f"{item['path'].split('_')[1]}[/]'"
            )
        else:
            icon = "📁" if item.get("type") == "directory" else "📄"
            tree.add(f"{icon} {item['path']}")
    console.print(Panel(tree, title="File Structure", border_style="cyan"))

    # Activity Stats
    stats = data["activity"]["stats"]
    stats_table = Table(title="Recent Activity (Last 7 Days)", box=None)
    stats_table.add_column("Stat", style="bold")
    stats_table.add_column("Value", style="green")
    stats_table.add_row("Commits", str(stats.get("commits_last_7d")))
    stats_table.add_row("Open PRs", str(stats.get("open_prs_count")))
    stats_table.add_row(
        "Active Contributors", str(stats.get("active_contributors_last_7d"))
    )
    console.print(stats_table)
