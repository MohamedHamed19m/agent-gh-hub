import os

from rich.console import Console
from rich.panel import Panel
from rich.syntax import Syntax

from gh_wrapper.commands.files import FileManager
from gh_wrapper.core.executor import GHExecutor

console = Console()


def read_specific_file(repo_name: str, file_path: str) -> None:
    executor = GHExecutor(repo=repo_name, use_cache=True)
    file_manager = FileManager(executor)

    # 1. Use a status spinner to bridge the 'gh' CLI execution time
    with console.status(
        f"[bold green]Pulling [cyan]{file_path}[/] from GitHub CLI bridge..."
    ):
        content = file_manager.get_file_content(file_path)

    if content:
        # 2. Auto-detect lexer based on file extension (e.g., .toml, .py)
        extension = os.path.splitext(file_path)[1].lstrip(".") or "text"

        # 3. Create a syntax-highlighted block
        # Theme 'monokai' is classic; 'ansi_dark' uses your terminal's colors
        syntax = Syntax(
            content, extension, theme="monokai", line_numbers=True, word_wrap=True
        )

        # 4. Wrap everything in a nice Panel
        console.print(
            Panel(
                syntax,
                title=f"[bold blue]File Content: {file_path}",
                subtitle=f"[dim]Repo: {repo_name}",
                border_style="bright_blue",
            )
        )
    else:
        console.print(
            f"[bold red]Error:[/] Could not retrieve content for {file_path}."
        )


if __name__ == "__main__":
    repo_name = "MohamedHamed19m/agent-gh-hub"
    # Testing with pyproject.toml to show off TOML highlighting
    read_specific_file(repo_name, "pyproject.toml")
