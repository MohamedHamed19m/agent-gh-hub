from rich.console import Console
from rich.panel import Panel
from rich.syntax import Syntax
from rich.table import Table

from gh_wrapper.commands.commits import CommitsManager
from gh_wrapper.core.executor import GHExecutor

console = Console()


def get_commit_details_from_repo(repo_name: str) -> None:
    executor = GHExecutor(repo=repo_name, use_cache=True)
    commits_manager = CommitsManager(executor)

    # NEW: Use RepoManager to get the actual default branch and its latest commit
    from gh_wrapper.commands.repository import RepoManager

    repo_manager = RepoManager(executor)

    with console.status("[bold green]Detecting default branch and latest commit..."):
        default_branch = repo_manager.get_default_branch()
        recent_commits = repo_manager._get_recent_commits(default_branch, limit=1)

    if not recent_commits:
        console.print(f"[bold red]Error:[/] No commits found in [white]{repo_name}[/].")
        return

    sha = recent_commits[0].get("sha")

    # 1. Show a spinner while the CLI works
    with console.status(
        f"[bold green]Fetching details for commit [white]{sha}[/] "
        f"in [white]{repo_name}[/]..."
    ):
        commit_details = commits_manager.get_commit_details(sha)

    if not commit_details:
        console.print(f"[bold red]Error:[/] No details found for commit {sha}.")
        return

    commit_info = commit_details.get("commit", {})
    author_info = commit_info.get("author", {})

    # 2. Header Panel
    header_content = (
        f"[bold cyan]SHA:[/] {commit_details.get('sha')}\n"
        f"[bold cyan]Author:[/] {author_info.get('name')}\n"
        f"[bold cyan]Date:[/] {author_info.get('date')}\n"
        f"[bold cyan]Message:[/] [italic white]{commit_info.get('message')}[/]"
    )
    console.print(
        Panel(
            header_content,
            title="[bold magenta]Commit Details",
            border_style="magenta",
            expand=False,
        )
    )

    # 3. Files Table
    files = commit_details.get("files", [])
    if files:
        table = Table(
            title="\n[bold]File Changes", show_header=True, header_style="bold yellow"
        )
        table.add_column("Filename", style="dim", width=40)
        table.add_column("Additions", justify="right", style="green")
        table.add_column("Deletions", justify="right", style="red")

        for file in files:
            table.add_row(
                file.get("filename"),
                f"+{file.get('additions')}",
                f"-{file.get('deletions')}",
            )
        console.print(table)

        # 4. Patch Syntax Highlighting
        console.print("\n[bold yellow]Diff Patches:[/bold yellow]")
        for file in files:
            if file.get("patch"):
                console.rule(f"[blue]{file.get('filename')}[/]")
                # Use "diff" lexer for syntax highlighting
                syntax = Syntax(
                    file.get("patch"), "diff", theme="monokai", line_numbers=True
                )
                console.print(syntax)
                console.print("")  # spacing


if __name__ == "__main__":
    # You can change these to test your specific Enterprise repo
    repo_name = "MohamedHamed19m/agent-gh-hub"
    get_commit_details_from_repo(repo_name)
