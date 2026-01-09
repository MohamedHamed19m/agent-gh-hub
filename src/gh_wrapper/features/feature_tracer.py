import logging
from typing import List, Optional, Union

from ..commands.commits import CommitsManager
from ..commands.files import FileManager
from ..commands.pull_requests import PRManager
from ..core.executor import GHExecutor
from ..models.trace import (
    FeatureTrace,
    FileMatch,
    MultiRepoFeatureTrace,
    TraceCommit,
    TracePR,
)

logger = logging.getLogger(__name__)


class FeatureTracer:
    """
    Feature layer for cross-sectional feature tracing across multiple repositories.
    """

    def __init__(self) -> None:
        """
        Initialize a stateless FeatureTracer.
        """
        pass

    def trace_feature(
        self,
        keyword: str,
        repos: Union[str, List[str]],
        branches: Optional[List[str]] = None,
        since: Optional[str] = None,
        search_files: bool = True,
        search_commits: bool = True,
        search_prs: bool = True,
        max_commits_per_branch: int = 100,
    ) -> MultiRepoFeatureTrace:
        """
        Trace a keyword across specified repositories and branches.

        Args:
            keyword: The phrase to search for.
            repos: Single repo string or list of repo strings.
            branches: List of branches to search. Defaults to ["main"].
            since: Optional date string (YYYY-MM-DD) to filter history.
            search_files: Whether to search code content.
            search_commits: Whether to search commit messages.
            search_prs: Whether to search PR titles and bodies.
            max_commits_per_branch: Limit commits fetched per branch.

        Returns:
            A MultiRepoFeatureTrace Pydantic model.
        """
        if isinstance(repos, str):
            repos = [repos]

        if not branches:
            branches = ["main"]

        multi_trace = MultiRepoFeatureTrace(
            keyword=keyword, repos_searched=repos, traces={}
        )

        for repo in repos:
            try:
                executor = GHExecutor(repo=repo)
                file_manager = FileManager(executor)
                commits_manager = CommitsManager(executor)
                pr_manager = PRManager(executor)

                trace = FeatureTrace(keyword=keyword, repo=repo)

                # 1. Search Files
                if search_files:
                    try:
                        file_results = file_manager.search_in_files(keyword)
                        trace.file_matches = [
                            FileMatch(
                                path=item["path"], match_snippet=item.get("snippet")
                            )
                            for item in file_results
                        ]
                    except AttributeError:
                        logger.warning(
                            f"FileManager.search_in_files not implemented. "
                            f"Skipping file search for {repo}."
                        )

                # 2. Search Commits
                if search_commits:
                    for branch in branches:
                        commits = commits_manager.get_commits_for_analysis(
                            branch=branch, since=since, limit=max_commits_per_branch
                        )
                        keyword_lower = keyword.lower()
                        for c in commits:
                            msg = c.get("commit", {}).get("message", "")
                            if keyword_lower in msg.lower():
                                author_data = c.get("commit", {}).get("author", {})
                                trace.commit_matches.append(
                                    TraceCommit(
                                        sha=c.get("sha", "")[:7],
                                        message=msg.split("\n")[0],
                                        author=author_data.get("name", "Unknown"),
                                        date=author_data.get("date", ""),
                                        branch=branch,
                                        is_merge=len(c.get("parents", [])) > 1,
                                    )
                                )

                # 3. Search PRs
                if search_prs:
                    prs = pr_manager.list_prs(state="all", limit=50)
                    keyword_lower = keyword.lower()
                    for pr in prs:
                        title = pr.get("title", "")
                        body = pr.get("body", "") or ""
                        if (
                            keyword_lower in title.lower()
                            or keyword_lower in body.lower()
                        ):
                            labels_data = pr.get("labels", [])
                            trace.pr_matches.append(
                                TracePR(
                                    number=pr.get("number"),
                                    title=title,
                                    author=pr.get("author", {}).get("login", "Unknown"),
                                    status=pr.get("state", "unknown"),
                                    created_at=pr.get("createdAt", ""),
                                    labels=[label.get("name") for label in labels_data]
                                    if isinstance(labels_data, list)
                                    else [],
                                    draft=pr.get("draft", False),
                                )
                            )

                multi_trace.traces[repo] = trace

            except Exception as e:
                logger.error(f"Failed to trace feature in {repo}: {e}")
                continue

        return multi_trace
