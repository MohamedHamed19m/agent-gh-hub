from typing import Any, Dict, List, Optional, cast

from ..core.executor import GHExecutor


class CommitsManager:
    def __init__(self, executor: GHExecutor):
        self.executor = executor

    def list_commits(
        self, branch: str = "main", limit: int = 10, path: Optional[str] = None
    ) -> List[Dict]:
        """List commits from a branch, optionally filtering by path"""
        # Use :owner/:repo placeholders which gh CLI resolves if local,
        # or use executor.repo if explicit
        if self.executor.repo:
            api_path = f"repos/{self.executor.repo}/commits"
        else:
            api_path = "repos/:owner/:repo/commits"

        params = ["api", api_path, "-F", f"sha={branch}", "-F", f"per_page={limit}"]

        if path:
            params.extend(["-F", f"path={path}"])

        result = self.executor.execute(params, parse_json=True)
        if isinstance(result, list):
            return cast(List[Dict[str, Any]], result)
        return []

    def search_commits(self, query: str, limit: int = 10) -> List[Dict]:
        """Search commits (using search api)"""
        q = f"{query}"
        if self.executor.repo:
            q += f" repo:{self.executor.repo}"

        params = ["api", "search/commits", "-F", f"q={q}", "-F", f"per_page={limit}"]
        result = self.executor.execute(params, parse_json=True)

        if isinstance(result, dict):
            return cast(List[Dict[str, Any]], result.get("items", []))
        return []

    def get_commit_details(self, sha: str) -> Dict:
        """Get details of a specific commit by SHA"""
        if self.executor.repo:
            api_path = f"repos/{self.executor.repo}/commits/{sha}"
        else:
            api_path = f"repos/:owner/:repo/commits/{sha}"

        params = ["api", api_path]
        result = self.executor.execute(params, parse_json=True)

        if isinstance(result, dict):
            return cast(Dict[str, Any], result)
        return {}
