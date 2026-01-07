from ..commands.commits import CommitsManager
from ..core.executor import GHExecutor


class AdvancedCommitSearcher:
    def __init__(self, executor: GHExecutor):
        self.manager = CommitsManager(executor)

    def search_in_current_repo(self, query: str):
        """Search commits in the current repository"""
        return self.manager.search_commits(query)
