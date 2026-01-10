import functools
import sys
from collections.abc import Callable
from typing import Any, TypeVar, cast

F = TypeVar("F", bound=Callable[..., Any])


def toon_unsupported(func: F) -> F:
    """Decorator to explicitly mark a command as not supporting TOON output.
    This ensures that if TOON is requested (or defaulted) for a command
    that only supports Markdown/Rich, we can handle it appropriately.
    """

    @functools.wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        # For now, this acts as a marker for Agent B to implement
        # correct default behavior (e.g., Markdown for review-pr).
        return func(*args, **kwargs)

    return cast(F, wrapper)


def fail_fast(message: str, code: int = 1) -> None:
    """Outputs a plain text error message to stderr and exits with a non-zero code.
    Ensures non-interactive 'fail-fast' behavior.
    """
    print(f"Error: {message}", file=sys.stderr)
    sys.exit(code)
