import sys

from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from rich.table import Table

from gh_wrapper.commands.pull_requests import PRManager
from gh_wrapper.core.executor import GHExecutor
from gh_wrapper.features.pr_review_analyzer import PrReviewAnalyzer
from gh_wrapper.models.pr_review import PrReviewInput

console = Console()


def main() -> None:
    # 1. Initialize core components
    executor = GHExecutor()
    pr_manager = PRManager(executor)
    analyzer = PrReviewAnalyzer(pr_manager)

    repo_display = executor.repo or "Local Repository"

    # Header Panel
    console.print(
        Panel(
            f"[bold cyan]PR Review Engine[/]\n"
            f"[bold white]Target:[/] {repo_display}",
            expand=False,
            border_style="cyan",
        )
    )

    # 2. Find a PR to demo if no ID provided
    pr_id = None
    if len(sys.argv) > 1:
        try:
            pr_id = int(sys.argv[1])
        except ValueError:
            console.print(f"[bold red]Invalid PR ID:[/] {sys.argv[1]}")
            return

    if pr_id is None:
        console.print("[yellow]No PR ID provided. Searching for latest open PR...[/]")
        prs = pr_manager.list_prs(state="open", limit=1)
        if not prs:
            console.print("[bold red]No open PRs found in the current repository.[/]")
            return
        pr_id = prs[0]["number"]
        console.print(f"[green]Found PR #[/]{pr_id}: [bold]{prs[0]['title']}[/]")

    # 3. Execution with Status Spinner
    try:
        with console.status(f"[bold green]Analyzing PR #{pr_id}..."):
            pr_input = PrReviewInput(
                repo_name=repo_display, pr_id=pr_id, review_depth="full"
            )
            report = analyzer.analyze_pr(pr_input)

        # 4. Display human-readable report
        markdown_report = analyzer.format_as_markdown(report)

        console.print("\n[bold]Generated PR Review Insights:[/]")
        console.print(
            Panel(
                Markdown(markdown_report),
                title=f"[bold green]PR Review Report - #{pr_id}",
                border_style="green",
                padding=(1, 2),
            )
        )

        # 5. Show structured metrics table
        metrics_table = Table(
            title="PR Metrics", show_header=True, header_style="bold magenta"
        )
        metrics_table.add_column("Metric")
        metrics_table.add_column("Value", justify="right")

        for key, value in report.metrics.items():
            metrics_table.add_row(key.replace("_", " ").capitalize(), str(value))

        console.print(metrics_table)

    except Exception as e:
        console.print(f"\n[bold red]❌ Error during PR review:[/]\n[dim]{e}[/]")


if __name__ == "__main__":
    main()
