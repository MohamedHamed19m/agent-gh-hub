from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from rich.table import Table

from gh_wrapper.core.executor import GHExecutor
from gh_wrapper.commands.pull_requests import PRManager
from gh_wrapper.features.pr_review_analyzer import PrReviewAnalyzer
from gh_wrapper.models.pr_review import PrReviewInput

console = Console()


def demo_pr_review() -> None:
    # 1. Initialize components
    executor = GHExecutor()
    pr_manager = PRManager(executor)
    analyzer = PrReviewAnalyzer(pr_manager)

    target_repo = "google-gemini/gemini-cli"

    # Header Panel
    console.print(
        Panel(
            f"[bold cyan]Automated PR Reviewer[/]\n"
            f"[bold white]Target Repository:[/] [yellow]{target_repo}[/]",
            expand=False,
            border_style="cyan",
        )
    )

    try:
        # 2. Find the latest open PR
        with console.status(f"[bold green]Fetching latest open PR from {target_repo}..."):
            latest_prs = pr_manager.list_prs(state="open", limit=1, repo=target_repo)

        if not latest_prs:
            console.print(f"[yellow]No open PRs found in {target_repo}.[/]")
            return

        latest_pr = latest_prs[0]
        pr_number = latest_pr["number"]
        pr_title = latest_pr["title"]
        
        console.print(f"[bold green]Found PR #{pr_number}:[/] {pr_title}")

        # 3. Analyze the PR
        pr_input = PrReviewInput(
            repo_name=target_repo,
            pr_id=pr_number
        )

        with console.status(f"[bold green]Analyzing PR #{pr_number}... (fetching diffs and patterns)"):
            result = analyzer.analyze_pr(pr_input)

        # 4. Display results
        markdown_report = analyzer.format_as_markdown(result)
        
        console.print("\n[bold]Review Report:[/]")
        console.print(
            Panel(
                Markdown(markdown_report),
                title=f"[bold green]PR Review: #{pr_number}",
                border_style="green",
                padding=(1, 2),
            )
        )

        # 5. Display Structured Data Summary (Metrics)
        metrics_table = Table(title="Metrics Summary", border_style="dim")
        metrics_table.add_column("Metric", style="magenta")
        metrics_table.add_column("Value", style="cyan")

        for key, value in result.metrics.items():
             metrics_table.add_row(key.replace("_", " ").title(), str(value))
        
        console.print(metrics_table)


    except Exception as e:
        console.print(f"\n[bold red]❌ Error during PR review:[/]\n[dim]{e}[/]")


if __name__ == "__main__":
    demo_pr_review()