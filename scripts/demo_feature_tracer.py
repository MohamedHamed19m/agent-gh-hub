from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from rich.table import Table

from gh_wrapper.features.feature_tracer import FeatureTracer

console = Console()


def demo_feature_tracer() -> None:
    # 1. Initialize tracer
    tracer = FeatureTracer()

    keyword = "CommitsManager"
    # For demo, we search in the current repo.
    # You can add other well-known repos if authenticated.
    repos = ["MohamedHamed19m/agent-gh-hub"]

    # Header Panel
    console.print(
        Panel(
            f"[bold cyan]Cross-Sectional Feature Tracer[/]\n"
            f"[bold white]Keyword:[/] [yellow]{keyword}[/",
            expand=False,
            border_style="cyan",
        )
    )

    # 2. Scope Table
    scope_table = Table(title="Search Scope", border_style="dim")
    scope_table.add_column("Repository", style="magenta")
    scope_table.add_column("Branches", style="green")

    for repo in repos:
        scope_table.add_row(repo, "main")

    console.print(scope_table)

    # 3. Execution
    try:
        with console.status(f"[bold green]Tracing '{keyword}' across repositories..."):
            report = tracer.trace_feature(
                keyword=keyword,
                repos=repos,
                branches=["main"],
                search_files=True,
                search_commits=True,
                search_prs=True,
            )

        # 4. Display human-readable report
        markdown_report = tracer.format_as_markdown(report)

        console.print("\n[bold]Trace Results:[/]")
        console.print(
            Panel(
                Markdown(markdown_report),
                title="[bold green]Feature Trace Report",
                border_style="green",
                padding=(1, 2),
            )
        )

        # 5. Show some detailed matches if found
        for repo_name, trace in report.traces.items():
            if trace.file_matches:
                console.print(f"\n[bold blue]File Matches in {repo_name}:[/]")
                for match in trace.file_matches[:3]:
                    console.print(f" • [dim]{match.path}[/]")

            if trace.commit_matches:
                console.print(f"\n[bold yellow]Commit Matches in {repo_name}:[/]")
                for commit in trace.commit_matches[:3]:
                    console.print(f" • [blue]{commit.sha}[/] {commit.message}")

    except Exception as e:
        console.print(f"\n[bold red]❌ Error during feature trace:[/]\n[dim]{e}[/]")


if __name__ == "__main__":
    demo_feature_tracer()
