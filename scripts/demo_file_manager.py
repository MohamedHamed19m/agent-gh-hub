from rich.console import Console
from rich.panel import Panel
from rich.syntax import Syntax
from rich.table import Table
from rich.tree import Tree

from gh_wrapper.commands.files import FileManager
from gh_wrapper.core.executor import GHExecutor

console = Console()


def demo_file_manager_capabilities(repo_name: str) -> None:
    executor = GHExecutor(repo=repo_name, use_cache=True)
    file_manager = FileManager(executor)

    console.print(
        Panel(
            f"Repository: [bold cyan]{repo_name}[/]\n"
            "Demonstrating [bold yellow]FileManager[/] capabilities",
            title="📂 FileManager Demo",
            border_style="green",
            expand=False,
        )
    )

    # 1. Listing files in the root
    with console.status("[bold green]Listing root directory..."):
        root_items = file_manager.list_files(path="", ref="main")

    if root_items:
        table = Table(
            title="Root Directory Content",
            show_header=True,
            header_style="bold magenta",
        )
        table.add_column("Type", width=10)
        table.add_column("Path", style="cyan")
        table.add_column("Size", justify="right")

        for item in root_items:
            icon = "📁" if item.get("type") == "dir" else "📄"
            size = f"{item.get('size')} B" if item.get("size") else "-"
            table.add_row(f"{icon} {item.get('type')}", item.get("path"), size)

        console.print(table)

    # 2. Listing files in a subdirectory (src/)
    with console.status("[bold green]Listing 'src' directory..."):
        src_items = file_manager.list_files(path="src", ref="main")

    if src_items:
        src_tree = Tree("📂 [bold blue]src/[/]")
        for item in src_items:
            icon = "📁" if item.get("type") == "dir" else "📄"
            src_tree.add(f"{icon} {item.get('name')}")

        console.print("\n[bold]Directory Tree View (src/):[/]")
        console.print(src_tree)

    # 3. Reading file content
    target_file = "pyproject.toml"
    with console.status(f"[bold green]Reading {target_file}..."):
        content = file_manager.get_file_content(target_file, ref="main")

    if content:
        console.print(f"\n[bold yellow]Content of {target_file}:[/]")
        # Limit preview for demo
        lines = content.splitlines()
        preview = "\n".join(lines[:15])
        if len(lines) > 15:
            preview += "\n..."

        syntax = Syntax(preview, "toml", theme="monokai", line_numbers=True)
        console.print(Panel(syntax, title=target_file, border_style="blue"))

    # 4. Reading file from a different reference (if applicable)
    # We'll try to list a directory on a different branch if we knew one,
    # but for demo we can just show how it would be called.
    console.print(
        "\n[bold]Pro Tip:[/] You can use the [italic]ref[/] parameter "
        "to list files or read content from any branch or tag."
    )
    console.print(
        "Example: [dim]file_manager.get_file_content('README.md', ref='develop')[/]"
    )


if __name__ == "__main__":
    repo_name = "MohamedHamed19m/agent-gh-hub"
    demo_file_manager_capabilities(repo_name)
