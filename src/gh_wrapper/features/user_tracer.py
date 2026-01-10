import concurrent.futures
import logging

from ..commands.commits import CommitsManager
from ..commands.repository import RepoManager
from ..commands.users import UserManager
from ..core.executor import GHExecutor
from ..models.trace import TraceCommit

logger = logging.getLogger(__name__)


class UserTracer:
    """Feature layer for tracing user activity across a repository."""

    def __init__(self, executor: GHExecutor):
        """Initialize with core dependencies."""
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
        branch: str | None = None,
    ) -> list[TraceCommit]:
        """Traces recent work for a user within a given repository."""
        self.executor.repo = repo

        # [1]. Identify target branches
        if branch:
            target_branches = [{"name": branch, "is_priority": True}]
        else:
            target_branches = self.repo_manager.get_combined_branches(branch_scan_limit)

        if not target_branches:
            logger.warning("No branches found in the repository.")
            return []

        # [2]. Parallel scan across branches
        user_commits = self.find_user_commits_in_branches_parallel(
            username, target_branches, commit_depth_per_branch
        )

        # [3]. Fallback to global search if no branch-level activity found
        if not user_commits:
            logger.info(
                f"No commits found for {username} in branch scans. "
                "Falling back to global search."
            )
            raw_global = self.commits_manager.get_user_commits_global_search(
                repo, username, limit
            )
            user_commits = [
                TraceCommit(
                    sha=c.get("sha", ""),
                    message=c.get("message", ""),
                    author=username,
                    date=c.get("date", ""),
                    branch="global search",
                    is_merge=False,
                )
                for c in raw_global
            ]

        return user_commits[:limit]

    def find_user_commits_in_branches_parallel(
        self, username: str, branches: list[dict], limit_per_branch: int
    ) -> list[TraceCommit]:
        """Find user commits across multiple branches in parallel"""
        results: dict[str, TraceCommit] = {}

        with concurrent.futures.ThreadPoolExecutor(
            max_workers=min(10, len(branches))
        ) as executor:
            future_to_branch = {
                executor.submit(
                    self.commits_manager.fetch_commits_from_branch,
                    b["name"],
                    username,
                    limit_per_branch,
                ): b
                for b in branches
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
                    logger.error(
                        f"Error fetching commits for branch {branch['name']}: {e}"
                    )

        final_list = list(results.values())
        final_list.sort(key=lambda x: x.date, reverse=True)
        return final_list
