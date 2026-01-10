import typer

app = typer.Typer(
    name="gh-bridge",
    help="Pythonic wrapper around GitHub CLI, optimized for AI agents and automation.",
    no_args_is_help=True,
    add_completion=False,
    rich_markup_mode="rich",
)
