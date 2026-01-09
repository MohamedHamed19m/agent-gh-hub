from rich import box
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from rich.table import Table

from gh_wrapper.commands.commits import CommitsManager
from gh_wrapper.core.executor import GHExecutor
from gh_wrapper.features.repo_analysis import RepoAnalyzer

console = Console()


def main() -> None:
    # 1. Initialize core components
    executor = GHExecutor()
    commits_manager = CommitsManager(executor)
    analyzer = RepoAnalyzer(commits_manager)

    repo_display = executor.repo or "Local Repository"

    # Header Panel
    console.print(
        Panel(
            f"[bold cyan]Repository Analysis Engine[/]\n"
            f"[bold white]Target:[/] {repo_display}",
            expand=False,
            border_style="cyan",
        )
    )

    # 2. Branch Information Table
    branches = ["main", "test-branch-fixture"]

    branch_table = Table(title="Analysis Scope", box=box.ROUNDED)
    branch_table.add_column("Property", style="bold magenta")
    branch_table.add_column("Value", style="yellow")

    branch_table.add_row("Target Branches", ", ".join(branches))
    branch_table.add_row("Timeframe", "Last 90 days")

    console.print(branch_table)

    # 3. Execution with Status Spinner
    try:
        with console.status(
            "[bold green]Fetching commit history and calculating patterns..."
        ):
            report = analyzer.analyze_commit_patterns(branches=branches, days_back=90)

        # 4. Display human-readable report
        # We use rich.markdown.Markdown to render the string beautifully in the terminal
        markdown_report = analyzer.format_as_markdown(report)

        console.print("\n[bold]Generated Insights:[/]")
        console.print(
            Panel(
                Markdown(markdown_report),
                title="[bold green]Analysis Report",
                border_style="green",
                padding=(1, 2),
            )
        )

    except Exception as e:
        console.print(f"\n[bold red]❌ Error during analysis:[/]\n[dim]{e}[/]")


if __name__ == "__main__":
    main()
