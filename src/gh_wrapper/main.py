"""Main entry point for the gh-bridge CLI.
Agent B: Implementation to unblock Phase 2.
"""

import sys

from rich.console import Console

from gh_wrapper.cli.main import app
from gh_wrapper.core.exceptions import GHWrapperError

# Agent B: Initialize Rich console for global error handling
console = Console(stderr=True)


def main() -> None:
    """Main execution function."""
    try:
        app()
    except GHWrapperError as e:
        # Agent B: User-facing errors must output plain text to stderr
        # with non-zero exit code
        print(f"Error: {str(e)}", file=sys.stderr)
        sys.exit(1)
    except Exception:
        # Agent B: Use uv/Rich traceback for uncaught exceptions as per spec
        console.print_exception()
        sys.exit(1)


if __name__ == "__main__":
    main()
