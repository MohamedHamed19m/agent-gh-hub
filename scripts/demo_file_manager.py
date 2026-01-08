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

    # NEW: Use RepoManager to get the actual default branch
    from gh_wrapper.commands.repository import RepoManager

    repo_manager = RepoManager(executor)

    with console.status("[bold green]Analyzing repository metadata..."):
        default_branch = repo_manager.get_default_branch()

    console.print(
        Panel(
            f"Repository: [bold cyan]{repo_name}[/]\n"
            f"Default Branch: [bold magenta]{default_branch}[/]\n"
            "Demonstrating [bold yellow]FileManager[/] capabilities",
            title="📂 FileManager Demo",
            border_style="green",
            expand=False,
        )
    )

    # 1. Listing files in the root
    with console.status(
        f"[bold green]Listing root directory (ref: {default_branch})..."
    ):
        root_items = file_manager.list_files(path="", ref=default_branch)

    if not root_items:
        console.print("[bold red]Error:[/] Could not list root items.")
        return

    table = Table(
        title="Root Directory Content",
        show_header=True,
        header_style="bold magenta",
    )
    table.add_column("Type", width=10)
    table.add_column("Path", style="cyan")
    table.add_column("Size", justify="right")

    first_dir = None
    first_file = None

    for item in root_items:
        i_type = item.get("type")
        i_path = item.get("path")

        if i_type == "dir" and not first_dir:
            first_dir = i_path
        # avoid binary-ish files
        if i_type == "file" and not first_file and i_path != "uv.lock":
            first_file = i_path

        icon = "📁" if i_type == "dir" else "📄"
        size = f"{item.get('size')} B" if item.get("size") else "-"
        table.add_row(f"{icon} {i_type}", i_path, size)

    console.print(table)

    # 2. Listing files in a subdirectory (Dynamic)
    if first_dir:
        with console.status(f"[bold green]Listing '{first_dir}' directory..."):
            dir_items = file_manager.list_files(path=first_dir, ref=default_branch)

        if dir_items:
            tree = Tree(f"📂 [bold blue]{first_dir}/[/]")
            for item in dir_items:
                icon = "📁" if item.get("type") == "dir" else "📄"
                tree.add(f"{icon} {item.get('name')}")

            console.print(f"\n[bold]Directory Tree View ({first_dir}/):[/]")
            console.print(tree)
        else:
            console.print(
                "\n[yellow]Note:[/] No subdirectories found in "
                f"'{first_dir}' to demonstrate tree view."
            )
    else:
        console.print(
            "\n[yellow]Note:[/] No subdirectories found to demonstrate tree view."
        )

    # 3. Reading file content (Dynamic)
    if first_file:
        with console.status(f"[bold green]Reading {first_file}..."):
            content = file_manager.get_file_content(first_file, ref=default_branch)

        if content:
            console.print(f"\n[bold yellow]Content of {first_file}:[/]")
            lines = content.splitlines()
            preview = "\n".join(lines[:15])
            if len(lines) > 15:
                preview += "\n..."

            # Auto-detect lexer based on extension
            ext = first_file.split(".")[-1] if "." in first_file else "txt"
            syntax = Syntax(preview, ext, theme="monokai", line_numbers=True)
            console.print(Panel(syntax, title=first_file, border_style="blue"))
    else:
        console.print(
            "\n[yellow]Note:[/] No files found to demonstrate content reading."
        )

    # 4. Reading file from a different reference (if applicable)
    # We'll try to list a directory on a different branch if we knew one,
    # but for demo we can just show how it would be called.
    console.print(
        "\n[bold]Pro Tip:[/] You can use the [italic]ref[/] parameter "
        "to list files or read content from any branch or tag."
    )
    console.print(
        "Example: [dim]file_manager.get_file_content('README.md', ref='develop')[/]]"
    )


if __name__ == "__main__":
    repo_name = "MohamedHamed19m/agent-gh-hub"
    demo_file_manager_capabilities(repo_name)
