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

        params = [
            "api",
            "--method",
            "GET",
            api_path,
            "-F",
            f"sha={branch}",
            "-F",
            f"per_page={limit}",
        ]

        if path:
            params.extend(["-F", f"path={path}"])

        result = self.executor.execute(params, parse_json=True)
        if isinstance(result, list):
            flattened = []
            for item in result:
                commit_obj = item.get("commit", {})
                author_obj = commit_obj.get("author", {})
                flattened.append(
                    {
                        "sha": item.get("sha"),
                        "message": commit_obj.get("message", "").split("\n")[0],
                        "author": author_obj.get("name"),
                        "date": author_obj.get("date"),
                        "url": item.get("html_url"),
                    }
                )
            return flattened
        return []

    def get_commits_for_analysis(
        self, branch: str, since: Optional[str] = None, limit: int = 100
    ) -> List[Dict]:
        """
        Get commits with full API response for analysis purposes.
        Does NOT flatten the response like list_commits().
        """
        if self.executor.repo:
            api_path = f"repos/{self.executor.repo}/commits"
        else:
            api_path = "repos/:owner/:repo/commits"

        params = [
            "api",
            "--method",
            "GET",
            api_path,
            "-F",
            f"sha={branch}",
            "-F",
            f"per_page={limit}",
        ]

        if since:
            params.extend(["-F", f"since={since}"])

        result = self.executor.execute(params, parse_json=True)
        if isinstance(result, list):
            return result
        return []

    def search_commits(self, query: str, limit: int = 10) -> List[Dict]:
        """Search commits (using search api)"""
        q = f"{query}"
        if self.executor.repo:
            q += f" repo:{self.executor.repo}"

        params = [
            "api",
            "--method",
            "GET",
            "search/commits",
            "-F",
            f"q={q}",
            "-F",
            f"per_page={limit}",
        ]
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

    def fetch_commits_from_branch(
        self, branch_name: str, user_search_term: str, limit_per_branch: int
    ) -> List[Dict]:
        """Fetch commits from a specific branch filtered by user search term"""
        local_results = []
        search_term_lower = user_search_term.lower()

        if self.executor.repo:
            base_path = f"repos/{self.executor.repo}/commits"
        else:
            base_path = "repos/:owner/:repo/commits"

        api_path = f"{base_path}?sha={branch_name}&per_page={limit_per_branch}"

        commits = self.executor.execute(["api", api_path], parse_json=True)

        if isinstance(commits, list):
            for c in commits:
                gh_user = c.get("author") or {}
                gh_login = (
                    (gh_user.get("login") or "").lower()
                    if gh_user and isinstance(gh_user, dict)
                    else ""
                )
                commit_obj = c.get("commit") or {}
                commit_meta = commit_obj.get("author") if commit_obj else None

                git_name = (
                    (commit_meta.get("name") or "").lower() if commit_meta else ""
                )
                git_email = (
                    (commit_meta.get("email") or "").lower() if commit_meta else ""
                )

                if (
                    search_term_lower in git_name
                    or search_term_lower in git_email
                    or (gh_login and search_term_lower == gh_login)
                ):
                    sha = c.get("sha") or ""
                    display_short = (
                        gh_login
                        if gh_login and gh_login != "app/"
                        else (git_email.split("@")[0] if git_email else "unknown")
                    )

                    local_results.append(
                        {
                            "sha_full": sha,
                            "branch": branch_name,
                            "sha": sha[:7],
                            "date": commit_meta.get("date") if commit_meta else "",
                            "short_name": display_short,
                            "message": commit_obj.get("message", "").split("\n")[0],
                            # "priority": is_p -> added later
                        }
                    )
        return local_results

    def get_user_commits_global_search(
        self, repo: str, username: str, limit: int = 10
    ) -> List[Dict]:
        """Fallback: Search commits globally in the repository for a user"""
        cmd = [
            "search",
            "commits",
            "--repo",
            repo,
            "--author",
            username,
            "--limit",
            str(limit),
            "--json",
            "sha,author,committer,message,url",
        ]

        results = self.executor.execute(cmd, parse_json=True)
        global_results = []
        if isinstance(results, list):
            for item in results:
                sha = item.get("sha", "")
                commit_obj = item.get("commit", {})
                commit_meta = commit_obj.get("author", {})

                message = commit_obj.get("message", "")

                branch_hint = "unknown/merged"

                if "Pull-Request-For: refs/heads/" in message:
                    branch_hint = (
                        message.split("Pull-Request-For: refs/heads/")[1]
                        .split()[0]
                        .strip()
                    )

                global_results.append(
                    {
                        "sha_full": sha,
                        "branch": branch_hint,
                        "sha": sha[:7],
                        "date": commit_meta.get("date", ""),
                        "short_name": username,
                        "message": message.split("\n")[0],
                        "priority": False,
                    }
                )
        return global_results
