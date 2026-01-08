from typing import Any, Dict, List, cast

from ..core.exceptions import GHCommandError
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
        repo_basics = self._get_repo_basics()
        default_branch = repo_basics.get("default_branch", "main")

        readme = self.file_manager.get_file_content("README.md", default_branch)
        active_prs = self.pr_manager.list_prs(state="open", limit=5)

        branches = self.list_branches(limit=10)

        file_structure = self._get_file_strcture(default_branch)
        recent_commits = self._get_recent_commits(default_branch, limit=5)

        readme_snippet = "No README.md found."
        if readme:
            readme_snippet = readme[:3000]
            if len(readme) > 3000:
                readme_snippet += "\n...[truncated]"

        return {
            "target": self.executor.repo,
            "metadata": {
                "default_branch": default_branch,
                "description": repo_basics.get("description"),
                "latest_release": repo_basics.get("latest_release"),
                "active_branches": [branch.get("name") for branch in branches]
                if isinstance(branches, list)
                else [],
            },
            "structure": file_structure,
            "activity": {
                "recent_commits": recent_commits,
                "active_pull_requests": active_prs,
            },
            "readme_snippet": readme_snippet,
        }

    def list_branches(self, limit: int = 10) -> List[Dict]:
        if self.executor.repo:
            api_path = f"repos/{self.executor.repo}/branches"
        else:
            api_path = "repos/:owner/:repo/branches"

        # params = ["api", api_path, "-F", f"per_page={limit}"]
        params = ["api", f"{api_path}?per_page={limit}"]
        result = self.executor.execute(params, parse_json=True)
        if isinstance(result, list):
            return cast(List[Dict[str, Any]], result)
        return []

    def _get_repo_basics(self) -> Dict[str, Any]:
        repo_target = self.executor.repo or ":owner/:repo"
        params = [
            "repo",
            "view",
            repo_target,
            "--json",
            "defaultBranchRef,description,latestRelease",
        ]
        result = self.executor.execute(params, parse_json=True)
        if isinstance(result, dict):
            return {
                "default_branch": (result.get("defaultBranchRef") or {}).get(
                    "name", "main"
                ),
                "description": result.get("description"),
                "latest_release": (result.get("latestRelease") or {}).get(
                    "tagName", "None"
                ),
            }
        return {}

    def _get_file_strcture(self, branch: str) -> List[Dict[str, Any]]:
        params = [
            "api",
            f"repos/{self.executor.repo}/contents?ref={branch}",
        ]
        result = self.executor.execute(params, parse_json=True)
        strcture = []
        if isinstance(result, list):
            for item in result:
                strcture.append(
                    {
                        "name": item.get("name"),
                        "path": item.get("path"),
                        "type": item.get("type"),
                    }
                )
        return strcture

    def _get_recent_commits(self, branch: str, limit: int = 5) -> List[Dict[str, Any]]:
        params = [
            "api",
            f"repos/{self.executor.repo}/commits?sha={branch}&per_page={limit}",
        ]
        result = self.executor.execute(params, parse_json=True)
        commits = []
        if isinstance(result, list):
            for item in result:
                commits.append(
                    {
                        "sha": item.get("sha")[:7] if item.get("sha") else "",
                        "message": item.get("commit", {}).get("message").split("\n")[0],
                        "author": item.get("commit", {}).get("author", {}).get("name"),
                        "date": item.get("commit", {}).get("author", {}).get("date"),
                    }
                )
        return commits

    def get_default_branch(self) -> str:
        """Gets the default branch name for the repository"""
        repo_basics = self._get_repo_basics()
        return str(repo_basics.get("default_branch", "main"))

    def get_priority_branches(self, priority_names: List[str]) -> List[Dict]:
        """Gets details of priority branches by their names and returns their SHA"""
        found_branches = []
        for name in priority_names:
            if self.executor.repo:
                api_path = f"repos/{self.executor.repo}/branches/{name}"
            else:
                api_path = f"repos/:owner/:repo/branches/{name}"

            params = ["api", api_path]
            try:
                result = self.executor.execute(params, parse_json=True)
                if isinstance(result, dict) and not result.get("_error"):
                    sha = result.get("commit", {}).get("sha", "")
                    if sha:
                        found_branches.append(
                            {"name": name, "sha": sha, "is_priority": True}
                        )
            except GHCommandError:
                # Log or print the error if needed, but continue to check other branches
                # print(f"Error fetching branch {name}: {e}")
                pass
        return found_branches

    def get_latest_branches_graphql(self, scan_limit: int = 50) -> List[Dict]:
        """Gets the latest branches using GraphQL to minimize API calls"""
        query = """
        query($owner: String!, $name: String!, $first: Int!) {
          repository(owner: $owner, name: $name) {
            refs(
              refPrefix: "refs/heads/",
              first: $first,
              orderBy: {field: TAG_COMMIT_DATE, direction: DESC}
            ) {
              nodes {
                name
                target {
                  ... on Commit {
                    oid
                    committedDate
                  }
                }
              }
            }
          }
        }
        """
        owner, repo_name = (
            self.executor.repo.split("/") if self.executor.repo else (":owner", ":repo")
        )

        # Pass variables individually
        # -f for String
        # -F for Int (typed)
        params = [
            "api",
            "graphql",
            "-f",
            f"query={query}",
            "-f",
            f"owner={owner}",
            "-f",
            f"name={repo_name}",
            "-F",
            f"first={scan_limit}",
        ]

        result = self.executor.execute(params, parse_json=True)
        branches = []
        if (
            isinstance(result, dict)
            and result.get("data")
            and result["data"].get("repository")
            and result["data"]["repository"].get("refs")
        ):
            for node in result["data"]["repository"]["refs"]["nodes"]:
                branches.append(
                    {
                        "name": node.get("name"),
                        "sha": node.get("target", {}).get("oid"),
                        "committed_date": node.get("target", {}).get("committedDate"),
                    }
                )
        return branches

    def get_combined_branches(self, scan_limit: int = 50) -> List[Dict]:
        """Combines priority branches and latest branches, avoiding duplicates"""
        priority_names = ["main", "master", "master_integration"]

        priority_branches = self.get_priority_branches(priority_names)
        latest_branches = self.get_latest_branches_graphql(scan_limit)

        combined = {branch["name"]: branch for branch in latest_branches}

        for p_branch in priority_branches:
            combined[p_branch["name"]] = p_branch

        return list(combined.values())
