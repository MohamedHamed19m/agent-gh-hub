import concurrent.futures
from typing import Dict, List, Optional

from ..commands.commits import CommitsManager
from ..commands.repository import RepoManager
from ..commands.users import UserManager
from ..core.executor import GHExecutor
from ..models.trace import TraceCommit


class UserTracer:
    def __init__(self, executor: GHExecutor):
        self.executor = executor
        self.user_manager = UserManager(executor)
        self.repo_manager = RepoManager(executor)
        self.commits_manager = CommitsManager(executor)

    def trace_recent_work(
        self,
        username: str,
        repo: str,
        limit: int = 10,
        branch_scan_limit: int = 10,
        commit_depth_per_branch: int = 100,
        branch: Optional[str] = None,
    ) -> List[TraceCommit]:
        """
        Traces recent work for a user within a given repository by analyzing
        their recent commits across branches and falling back to global
        search if needed.
        """
        self.executor.repo = repo

        # [1]. Get Combined branches
        if branch:
            target_branches = [{"name": branch, "is_priority": True}]
        else:
            target_branches = self.repo_manager.get_combined_branches(branch_scan_limit)

        if not target_branches:
            print("No branches found in the repository.")
            return []

        # [2]. Find user commits in parallel across branches
        user_commits = self.find_user_commits_in_branches_parallel(
            username, target_branches, commit_depth_per_branch
        )

        # [3]. If no commits found, fallback to global commit search
        if not user_commits:
            print(
                f"No commits found for user {username} in the repository "
                "branches. Falling back to global search."
            )
            raw_global = self.commits_manager.get_user_commits_global_search(
                repo, username, limit
            )
            # Convert raw global search results to TraceCommit
            user_commits = []
            for c in raw_global:
                user_commits.append(
                    TraceCommit(
                        sha=c.get("sha", ""),
                        message=c.get("message", ""),
                        author=username,
                        date=c.get("date", ""),
                        branch="unknown (global search)",
                        is_merge=False,
                    )
                )

        # [4]. Limit results
        return user_commits[:limit]

    def find_user_commits_in_branches_parallel(
        self, username: str, branches: List[dict], limit_per_branch: int
    ) -> List[TraceCommit]:
        """Find user commits across multiple branches in parallel"""
        results = {}
        with concurrent.futures.ThreadPoolExecutor(
            max_workers=min(10, len(branches))
        ) as executor:
            future_to_branch = {
                executor.submit(
                    self.commits_manager.fetch_commits_from_branch,
                    branch["name"],
                    username,
                    limit_per_branch,
                ): branch
                for branch in branches
            }

            for future in concurrent.futures.as_completed(future_to_branch):
                branch = future_to_branch[future]
                try:
                    branch_commits = future.result()
                    for c in branch_commits:
                        sha = c.get("sha_full")
                        if sha and sha not in results:
                            results[sha] = TraceCommit(
                                sha=sha,
                                message=c.get("message", ""),
                                author=username,
                                date=c.get("date", ""),
                                branch=branch["name"],
                                is_merge=c.get("is_merge", False),
                            )
                except Exception as e:
                    # in a real logging scenario, log the exception
                    print(f"Error fetching commits for branch {branch['name']}: {e}")

        final_list = list(results.values())
        # sort by date in descending order
        final_list.sort(key=lambda x: x.date, reverse=True)
        return final_list
