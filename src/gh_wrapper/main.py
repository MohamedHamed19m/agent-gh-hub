from gh_wrapper.cli.main import app


def main() -> None:
    """Main entry point for the CLI."""
    try:
        from rich.traceback import install

        install(show_locals=False)
    except ImportError:
        pass

    app()


if __name__ == "__main__":
    main()
