from typing import Dict, List

from ..commands.users import UserManager
from ..core.executor import GHExecutor


class UserTracer:
    def __init__(self, executor: GHExecutor):
        self.executor = executor
        self.user_manager = UserManager(executor)

    def trace_recent_work(self, username: str, limit: int = 10) -> List[Dict]:
        """Get recent push events and commits to understand what they are working on"""
        events = self.user_manager.get_user_activity(username, limit=limit)

        # Filter for relevant events
        relevant_types = ["PushEvent", "PullRequestEvent", "CreateEvent"]
        filtered = [e for e in events if e["type"] in relevant_types]

        return filtered
