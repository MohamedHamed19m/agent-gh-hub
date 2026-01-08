from rich.console import Console
from rich.panel import Panel
from rich.tree import Tree

from gh_wrapper.core.executor import GHExecutor
from gh_wrapper.features.user_tracer import UserTracer

console = Console()


def trace_user_activity(username: str, repo_name: str, limit: int = 10) -> None:
    try:
        executor = GHExecutor(repo=repo_name, use_cache=True)
        user_tracer = UserTracer(executor)

        with console.status(
            f"[bold green]Tracing activity for [white]{username}[/]..."
        ):
            recent_work = user_tracer.trace_recent_work(username, repo_name, limit)

        # 1. Header Section
        console.print(
            Panel(
                f"Target User: [bold yellow]{username}[/]\n"
                f"Repository: [bold cyan]{repo_name}[/]\n"
                f"Limit: [dim]{limit} events[/]",
                title="👤 [bold]User Activity Tracer",
                border_style="yellow",
                expand=False,
            )
        )

        if recent_work:
            # 2. Create a Timeline using a Tree
            timeline = Tree("[bold magenta]Activity Timeline")

            for commit in recent_work:
                display_date = (
                    commit.get("date", "")[:10]
                    if commit.get("date")
                    else "unknown date"
                )
                sha = commit.get("sha", "N/A")[:7]
                msg = commit.get("message", "No message")
                branch = commit.get("branch", "unknown")

                # Highlight priority work if your tracer supports it
                color = "green" if commit.get("priority") else "white"

                # Add a node for each event
                event_node = timeline.add(
                    f"[bold blue]{display_date}[/] | [dim]{sha}[/] | "
                    f"[bold {color}]{msg}[/]"
                )
                event_node.add(f"[dim]Branch:[/] [cyan]{branch}[/]")

            console.print(timeline)

            # 3. Summary Statistics
            unique_branches = set(
                c.get("branch") for c in recent_work if c.get("branch")
            )
            console.print(
                f"\n[bold]Summary:[/] User worked across "
                f"[bold cyan]{len(unique_branches)}[/] branches."
            )

        else:
            console.print(
                f"[bold red]![/] No recent work found for [bold]{username}[/]."
            )

    except Exception as e:
        console.print(f"[bold red]Error tracing user activity:[/] {e}")


if __name__ == "__main__":
    repo_name = "MohamedHamed19m/agent-gh-hub"
    trace_user_activity("MohamedHamed19m", repo_name, limit=10)
