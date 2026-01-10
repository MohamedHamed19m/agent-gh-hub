from typing import Any

from pydantic import BaseModel, Field

from gh_wrapper.commands.commits import CommitsManager
from gh_wrapper.core.executor import GHExecutor


class BranchStats(BaseModel):
    """Data model for branch analytics statistics."""

    branch: str
    total_commits: int
    last_commit: dict[str, Any] | None = None
    contributors: dict[str, int] = Field(default_factory=dict)
    health_score: float = 0.0


class BranchAnalyzer:
    """Analyzes branch activity and health using the GitHub CLI."""

    def __init__(self, executor: GHExecutor):
        self.executor = executor
        self.commits_manager = CommitsManager(executor)

    def analyze_branch(self, branch: str, limit: int = 100) -> BranchStats:
        """Analyzes the given branch and returns a BranchStats object."""
        commits = self.commits_manager.list_commits(branch=branch, limit=limit)

        if not commits:
            return BranchStats(branch=branch, total_commits=0)

        total_commits = len(commits)
        contributors: dict[str, int] = {}

        # Last commit is usually the first in the list
        first_commit = commits[0]
        last_commit_info = {
            "sha": first_commit.get("sha"),
            "author": first_commit.get("author"),
            "date": first_commit.get("date"),
        }

        for commit in commits:
            author_name = commit.get("author") or "Unknown"
            contributors[author_name] = contributors.get(author_name, 0) + 1

        # Simple health score logic:
        # (Very basic placeholder: More contributors = higher score, capped at 100)
        health_contribution = float(len(contributors)) * 10
        commit_contribution = total_commits / 10
        health_score = min(100.0, health_contribution + commit_contribution)

        return BranchStats(
            branch=branch,
            total_commits=total_commits,
            last_commit=last_commit_info,
            contributors=contributors,
            health_score=health_score,
        )
