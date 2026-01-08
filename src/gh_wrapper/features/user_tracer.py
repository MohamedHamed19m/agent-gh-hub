import concurrent.futures
from typing import Dict, List

from ..commands.commits import CommitsManager
from ..commands.repository import RepoManager
from ..commands.users import UserManager
from ..core.executor import GHExecutor


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
    ) -> List[Dict]:
        """
        Traces recent work for a user within a given repository by analyzing
        their recent commits across branches and falling back to global
        search if needed.
        """
        self.executor.repo = repo

        # [1]. Get Combined branches
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
            user_commits = self.commits_manager.get_user_commits_global_search(
                repo, username, limit
            )

        # [4]. Limit results
        return user_commits[:limit]

    def find_user_commits_in_branches_parallel(
        self, username: str, branches: List[dict], limit_per_branch: int
    ) -> List[Dict]:
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
                    for commit in branch_commits:
                        commit["priority"] = branch.get("is_priority", False)

                    for c in branch_commits:
                        if c["sha_full"] not in results:
                            results[c["sha_full"]] = c
                except Exception as e:
                    # in a real logging scenario, log the exception
                    print(f"Error fetching commits for branch {branch['name']}: {e}")

        final_list = list(results.values())
        # sort by date in descending order
        final_list.sort(key=lambda x: x.get("date", ""), reverse=True)
        return final_list
