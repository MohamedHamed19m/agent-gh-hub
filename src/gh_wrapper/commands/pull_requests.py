from typing import Any, Dict, List, cast

from ..core.executor import GHExecutor


class PRManager:
    def __init__(self, executor: GHExecutor):
        self.executor = executor

    def list_prs(
        self, state: str = "open", limit: int = 10, repo: str | None = None
    ) -> List[Dict]:
        """List pull requests"""
        cmd = [
            "pr",
            "list",
            "--state",
            state,
            "--limit",
            str(limit),
            "--json",
            "number,title,url,author,createdAt,state,headRefName,baseRefName",
        ]
        if repo:
            cmd.extend(["-R", repo])

        result = self.executor.execute(cmd, parse_json=True)
        if isinstance(result, list):
            return cast(List[Dict[str, Any]], result)
        return []

    def get_pr_content(self, number: int, repo: str | None = None) -> Dict:
        """Get PR details"""
        cmd = [
            "pr",
            "view",
            str(number),
            "--json",
            "number,title,body,comments,reviews,files",
        ]
        if repo:
            cmd.extend(["-R", repo])

        result = self.executor.execute(cmd, parse_json=True)
        if isinstance(result, dict):
            return cast(Dict[str, Any], result)
        return {}

    def get_pr_diff(
        self,
        pr_number: int,
        target_branch: str | None = None,
        repo: str | None = None,
    ) -> str:
        """Get PR diff content in patch format."""
        cmd = [
            "pr",
            "diff",
            str(pr_number),
            "--patch",
        ]
        if target_branch:
            cmd.extend(["--base", target_branch])
        if repo:
            cmd.extend(["-R", repo])

        result = self.executor.execute(cmd, parse_json=False)
        return cast(str, result)

    def get_pr_diff_against_branch(
        self, number: int, target_branch: str, repo: str | None = None
    ) -> str:
        """Get PR diff against a specific target branch in patch format"""
        cmd = [
            "pr",
            "diff",
            str(number),
            "--base",
            target_branch,
            "--patch",
        ]
        if repo:
            cmd.extend(["-R", repo])

        result = self.executor.execute(cmd)
        return str(result)
