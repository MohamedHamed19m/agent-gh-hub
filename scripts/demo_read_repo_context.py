"""
TEMPORARILY DISABLED: This demo requires RepoContextAnalyzer which has been
moved to a future track (features/repo_context.py) after the RepoManager refactor.
"""

# from rich import box
# from rich.columns import Columns
# from rich.console import Console
# from rich.panel import Panel
# from rich.table import Table
# from rich.tree import Tree

# from gh_wrapper.core.executor import GHExecutor
# from gh_wrapper.features.repo_context import RepoContextAnalyzer

# console = Console()


# def read_repo_context(repo_name: str) -> None:
#     executor = GHExecutor(repo=repo_name, use_cache=True)
#     analyzer = RepoContextAnalyzer(executor)

#     with console.status(
#         f"[bold green]Generating deep context for [white]{repo_name}[/]..."
#     ):
#         context = analyzer.analyze_current_context()

#     if not context:
#         console.print("[bold red]Error:[/] Could not analyze repository.")
#         return

#     # 1. Header & Metadata Section
#     metadata = context.get("metadata", {})
#     meta_table = Table(show_header=False, box=box.SIMPLE)
#     meta_table.add_row("[bold cyan]Default Branch:", metadata.get("default_branch"))
#     meta_table.add_row(
#         "[bold cyan]Latest Release:", str(metadata.get("latest_release") or "None")
#     )
#     meta_table.add_row("[bold cyan]Description:", metadata.get("description", "N/A"))

#     active_branches = ", ".join(metadata.get("active_branches", []))
#     meta_table.add_row("[bold cyan]Active Branches:", f"[yellow]{active_branches}[/]")

#     console.print(
#         Panel(
#             meta_table,
#             title=f"[bold magenta]Repo: {repo_name}",
#             border_style="magenta",
#         )
#     )

#     # 2. File Structure (Tree View)
#     structure_tree = Tree(f"[bold blue]📂 {context.get('target')}")
#     structure = context.get("structure", [])
#     for i, item in enumerate(structure):
#         if i >= 15:
#             structure_tree.add("[dim]... (truncated)[/]")
#             break
#         icon = "📄" if item.get("type") == "file" else "📁"
#         structure_tree.add(f"{icon} {item.get('path')}")

#     # 3. Activity Section (Commits & PRs)
#     activity = context.get("activity", {})

#     # Commits List
#     commit_list = ""
#     for commit in activity.get("recent_commits", [])[:5]:
#         commit_list += f"• [blue]{commit.get('sha')[:7]}[/] {commit.get('message')}\n"

#     # PRs List
#     pr_list = ""
#     for pr in activity.get("open_prs", [])[:5]:
#         pr_list += f"• [green]#{pr.get('number')}[/] {pr.get('title')}\n"

#     # Layout with Columns
#     activity_panel = Panel(
#         f"[bold yellow]Recent Commits[/]\n{commit_list or 'None'}\n"
#         f"[bold green]Open PRs[/]\n{pr_list or 'None'}",
#         title="[bold]Activity",
#         border_style="yellow",
#     )

#     console.print(Columns([structure_tree, activity_panel]))

#     # 4. README Snippet
#     if context.get("readme_snippet"):
#         console.print(
#             Panel(
#                 context.get("readme_snippet"),
#                 title="[bold]README Preview",
#                 border_style="dim",
#                 height=12,
#             )
#         )


# if __name__ == "__main__":
#     repo_name = "MohamedHamed19m/agent-gh-hub"
#     read_repo_context(repo_name)
