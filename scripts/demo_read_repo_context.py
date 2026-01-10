from rich import box
from rich.columns import Columns
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.tree import Tree

from gh_wrapper.core.executor import GHExecutor
from gh_wrapper.features.repo_context import RepoContextAnalyzer

console = Console()


def read_repo_context(repo_name: str) -> None:
    executor = GHExecutor(repo=repo_name, use_cache=True)
    analyzer = RepoContextAnalyzer(executor)

    with console.status(
        f"[bold green]Generating AI-optimized context for [white]{repo_name}[/]..."
    ):
        context = analyzer.analyze_current_context()

    if not context:
        console.print("[bold red]Error:[/] Could not analyze repository.")
        return

    # 1. Header & Metadata Section
    metadata = context.metadata
    meta_table = Table(show_header=False, box=box.SIMPLE)
    meta_table.add_row("[bold cyan]Default Branch:", metadata.default_branch)
    meta_table.add_row(
        "[bold cyan]Latest Release:", str(metadata.latest_release or "None")
    )
    meta_table.add_row(
        "[bold cyan]Stars/Forks:",
        f"⭐ {metadata.stars} / 🍴 {metadata.forks}",
    )
    meta_table.add_row("[bold cyan]Description:", metadata.description or "N/A")

    topics = ", ".join(metadata.topics)
    if topics:
        meta_table.add_row("[bold cyan]Topics:", f"[yellow]{topics}[/]")

    console.print(
        Panel(
            meta_table, title=f"[bold magenta]Repo: {repo_name}", border_style="magenta"
        )
    )

    # 2. File Structure (Tree View)
    structure_tree = Tree(f"[bold blue]📂 {context.target}")
    structure = context.structure
    for item in structure:
        if item.type == "truncated":
            structure_tree.add(f"[dim]... {item.count} more items in {item.path}[/]")
            continue

        icon = "📄" if item.type == "file" else "📁"
        priority_marker = "[bold green]! [/]" if item.priority else ""
        structure_tree.add(f"{priority_marker}{icon} {item.path}")

    # 3. Activity Section (Commits & PRs)
    activity = context.activity
    stats = activity.stats

    # Commits List
    commit_list = f"[bold white]Last 7 Days:[/] {stats.commits_last_7d} commits\n\n"
    for commit in activity.recent_commits[:5]:
        merge_marker = " 🔀" if commit.is_merge else ""
        commit_list += f"• [blue]{commit.sha[:7]}[/] {commit.message}{merge_marker}\n"

    # PRs List
    pr_list = f"[bold white]Open PRs:[/] {stats.open_prs_count}\n\n"
    for pr in activity.open_pull_requests[:5]:
        status_color = "green" if pr.status == "Open" else "yellow"
        pr_list += f"• [bold {status_color}]#{pr.number}[/] {pr.title}\n"

    # Layout with Columns
    activity_panel = Panel(
        f"{commit_list}\n{pr_list}",
        title="[bold yellow]Activity & Stats",
        border_style="yellow",
    )

    console.print(Columns([structure_tree, activity_panel]))

    # 4. README Snippet
    readme = context.readme_snippet
    if readme:
        console.print(
            Panel(
                readme,
                title="[bold]README Preview (Truncated)",
                border_style="dim",
                height=15,
            )
        )


if __name__ == "__main__":
    repo_name = "MohamedHamed19m/agent-gh-hub"
    read_repo_context(repo_name)
