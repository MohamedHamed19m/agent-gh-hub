from typing import Any, Dict, List, cast

from ..core.executor import GHExecutor


class UserManager:
    def __init__(self, executor: GHExecutor):
        self.executor = executor

    def get_user_activity(self, username: str, limit: int = 10) -> List[Dict]:
        """Get public events for a user"""
        params = ["api", f"users/{username}/events", "-F", f"per_page={limit}"]
        result = self.executor.execute(params, parse_json=True)
        if isinstance(result, list):
            return cast(List[Dict[str, Any]], result)
        return []

    def get_user_commits(self, username: str, limit: int = 10) -> List[Dict]:
        """Search commits by user.

        (global search or repo context if specified in executor?)
        search/commits is global unless repo: is in q.
        """
        q = f"author:{username}"
        if self.executor.repo:
            q += f" repo:{self.executor.repo}"

        params = ["api", "search/commits", "-F", f"q={q}", "-F", f"per_page={limit}"]
        result = self.executor.execute(params, parse_json=True)

        if isinstance(result, dict):
            return cast(List[Dict[str, Any]], result.get("items", []))
        return []
