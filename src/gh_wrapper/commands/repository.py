import concurrent.futures
from typing import Any, cast

from ..core.exceptions import GHCommandError
from ..core.executor import GHExecutor


class RepoManager:
    def __init__(self, executor: GHExecutor, max_concurrent: int = 6):
        self.executor = executor
        self.max_concurrent = max_concurrent

    # TODO: get_context() removed - orchestration logic belongs in
    # features/repo_context.py and will be implemented in a future track.

    def list_branches(self, limit: int = 10) -> list[dict[str, Any]]:
        """Lists branches in the repository using GitHub API.

        Args:
            limit: Maximum number of branches to return. Defaults to 10.

        Returns:
            A list of branch dictionaries from the GitHub API.

        """
        if self.executor.repo:
            api_path = f"repos/{self.executor.repo}/branches"
        else:
            api_path = "repos/:owner/:repo/branches"

        # params = ["api", api_path, "-F", f"per_page={limit}"] (old code)
        params = ["api", f"{api_path}?per_page={limit}"]
        result = self.executor.execute(params, parse_json=True)
        if isinstance(result, list):
            return cast(list[dict[str, Any]], result)
        return []

    def get_repo_basics(self) -> dict[str, Any]:
        """Gets basic repository metadata using 'gh repo view'.

        Returns:
            A dictionary containing 'default_branch', 'description',
            'latest_release', 'stargazerCount', 'forkCount', 'isFork',
            'isArchived', and 'topics'.

        """
        repo_target = self.executor.repo or ":owner/:repo"
        params = [
            "repo",
            "view",
            repo_target,
            "--json",
            "defaultBranchRef,description,latestRelease,stargazerCount,forkCount,isFork,isArchived,repositoryTopics",
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
                "stars": result.get("stargazerCount", 0),
                "forks": result.get("forkCount", 0),
                "is_fork": result.get("isFork", False),
                "is_archived": result.get("isArchived", False),
                "topics": [t.get("name") for t in result.get("repositoryTopics", [])]
                if isinstance(result.get("repositoryTopics"), list)
                else [],
            }
        return {}

    def get_file_structure(self, branch: str) -> list[dict[str, Any]]:
        """Gets the recursive file structure of a repository at a specific branch.

        Args:
            branch: The branch name to inspect.

        Returns:
            A list of dictionaries containing 'path', 'type', and 'sha' for each item.

        """
        params = [
            "api",
            f"repos/{self.executor.repo}/git/trees/{branch}?recursive=1",
        ]
        result = self.executor.execute(params, parse_json=True)
        structure = []
        if isinstance(result, dict) and "tree" in result:
            for item in result["tree"]:
                structure.append(
                    {
                        "path": item.get("path"),
                        "type": "file" if item.get("type") == "blob" else "dir",
                        "sha": item.get("sha"),
                    }
                )
        return structure

    def get_recent_commits(self, branch: str, limit: int = 5) -> list[dict[str, Any]]:
        """Gets recent commits for a specific branch.

        Args:
            branch: The branch name to inspect.
            limit: Maximum number of commits to return. Defaults to 5.

        Returns:
            A list of dictionaries containing 'sha', 'message', 'author', and 'date'.

        """
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
        """Gets the default branch name for the repository.

        Returns:
            The name of the default branch (e.g., 'main').

        """
        repo_basics = self.get_repo_basics()
        return str(repo_basics.get("default_branch", "main"))

    def _fetch_branch_details(self, name: str) -> dict[str, Any] | None:
        """Internal worker to fetch single branch details for threading.

        Args:
            name: Branch name to fetch.

        Returns:
            Dictionary with branch info or None if failed.

        """
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
                    return {"name": name, "sha": sha, "is_priority": True}
        except GHCommandError:
            pass
        except Exception:
            # Catch-all for robustness within thread
            pass
        return None

    def get_priority_branches(self, priority_names: list[str]) -> list[dict[str, Any]]:
        """Gets details of priority branches by their names and returns their SHA.

        Uses threaded execution to fetch branches in parallel.

        Args:
            priority_names: A list of branch names to check.

        Returns:
            A list of dictionaries for each found priority branch.

        """
        found_branches = []

        with concurrent.futures.ThreadPoolExecutor(
            max_workers=self.max_concurrent
        ) as executor:
            future_to_branch = {
                executor.submit(self._fetch_branch_details, name): name
                for name in priority_names
            }
            for future in concurrent.futures.as_completed(future_to_branch):
                result = future.result()
                if result:
                    found_branches.append(result)

        return found_branches

    def get_latest_branches_graphql(self, scan_limit: int = 50) -> list[dict[str, Any]]:
        """Gets the latest branches using GraphQL to minimize API calls.

        Args:
            scan_limit: Maximum number of branches to fetch. Defaults to 50.

        Returns:
            A list of dictionaries containing branch name, SHA, and committed date.

        """
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

    def get_combined_branches(self, scan_limit: int = 50) -> list[dict[str, Any]]:
        """Combines priority branches and latest branches, avoiding duplicates.

        Args:
            scan_limit: Maximum number of latest branches to scan. Defaults to 50.

        Returns:
            A combined list of priority and recently updated branches.

        """
        priority_names = ["main", "master", "master_integration"]

        priority_branches = self.get_priority_branches(priority_names)
        latest_branches = self.get_latest_branches_graphql(scan_limit)

        combined = {branch["name"]: branch for branch in latest_branches}

        for p_branch in priority_branches:
            combined[p_branch["name"]] = p_branch

        return list(combined.values())
