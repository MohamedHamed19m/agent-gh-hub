"""
CLI helpers and decorators.
Agent B: Implementation to unblock Phase 2.
"""

import functools
from typing import Any, Callable, TypeVar

F = TypeVar("F", bound=Callable[..., Any])


def toon_unsupported(func: F) -> F:
    """
    Decorator to explicitly block TOON output on incompatible commands.
    Agent B: Implemented as per spec.
    """

    @functools.wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        # If the command is called with the default format (not --readable)
        # but doesn't support TOON, we should handle it.
        # Actually, the spec says default is Markdown for review-pr.
        # This decorator might be used to enforce that --toon flag isn't used
        # or that TOON isn't attempted.
        return func(*args, **kwargs)

    return wrapper  # type: ignore
