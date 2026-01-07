from typing import Dict, List

from ..core.executor import GHExecutor
from .files import FileManager
from .pull_requests import PRManager


class RepoManager:
    def __init__(self, executor: GHExecutor):
        self.executor = executor
        self.pr_manager = PRManager(executor)
        self.file_manager = FileManager(executor)

    def get_context(self) -> Dict:
        """Get high level context: readme, active PRs, recent branches"""
        readme = self.file_manager.get_file_content("README.md")

        active_prs = self.pr_manager.list_prs(state="open", limit=5)

        branches = self.list_branches(limit=10)

        return {
            "readme_preview": readme[:500] + "..." if len(readme) > 500 else readme,
            "active_prs": active_prs,
            "branches": [b.get("name") for b in branches]
            if isinstance(branches, list)
            else [],
        }

    def list_branches(self, limit: int = 10) -> List[Dict]:
        if self.executor.repo:
            api_path = f"repos/{self.executor.repo}/branches"
        else:
            api_path = "repos/:owner/:repo/branches"

        params = ["api", api_path, "-F", f"per_page={limit}"]
        return self.executor.execute(params, parse_json=True)
