from typing import Any, Dict

from ..commands.repository import RepoManager
from ..core.executor import GHExecutor


class RepoContextAnalyzer:
    def __init__(self, executor: GHExecutor):
        self.manager = RepoManager(executor)

    def analyze_current_context(self) -> Dict[str, Any]:
        """Analyze repository context"""
        return self.manager.get_context()
