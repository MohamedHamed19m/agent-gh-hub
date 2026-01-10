import logging
from datetime import datetime, timedelta
from typing import Any

from ..commands.commits import CommitsManager
from ..commands.files import FileManager
from ..commands.pull_requests import PRManager
from ..commands.repository import RepoManager
from ..core.executor import GHExecutor
from ..models.analysis import (
    RepoContextActivity,
    RepoContextMetadata,
    RepoContextReport,
    RepoContextStats,
    RepoContextStructureItem,
)
from ..models.trace import TraceCommit, TracePR

logger = logging.getLogger(__name__)


class RepoContextAnalyzer:
    """
    Feature layer for generating AI-optimized repository snapshots.

    Composes RepoManager, PRManager, and FileManager to aggregate
    metadata, file structure, activity, and documentation into a
    single RepoContextReport model.
    """

    PRIORITY_WHITELIST = [
        # Config
        "pyproject.toml",
        "setup.py",
        "package.json",
        "tsconfig.json",
        # Docker
        "Dockerfile",
        "docker-compose.yml",
        ".dockerignore",
        # CI/CD
        ".github/workflows/",
        ".gitlab-ci.yml",
        "Jenkinsfile",
        # Docs
        "README.md",
        "CHANGELOG.md",
        "CONTRIBUTING.md",
        "LICENSE",
        # Other
        ".gitignore",
        "Makefile",
    ]

    def __init__(self, executor: GHExecutor):
        """
        Initialize with core dependencies.
        """
        self.executor = executor
        self.repo_manager = RepoManager(executor)
        self.pr_manager = PRManager(executor)
        self.file_manager = FileManager(executor)
        self.commits_manager = CommitsManager(executor)

    def analyze_current_context(self, branch: str | None = None) -> RepoContextReport:
        """
        Generate a comprehensive snapshot of the repository state.
        """
        # Phase 1: Metadata
        raw_metadata = self.repo_manager.get_repo_basics()
        default_branch = branch or raw_metadata.get("default_branch", "main")

        metadata = RepoContextMetadata(
            default_branch=raw_metadata.get("default_branch", "main"),
            description=raw_metadata.get("description"),
            latest_release=raw_metadata.get("latest_release"),
            stars=raw_metadata.get("stargazers_count", 0),
            forks=raw_metadata.get("forks_count", 0),
            is_fork=raw_metadata.get("fork", False),
            is_archived=raw_metadata.get("archived", False),
            topics=raw_metadata.get("topics", []),
        )

        # Phase 2: Structure
        raw_structure = self._get_smart_structure(default_branch)
        structure = [RepoContextStructureItem(**item) for item in raw_structure]

        # Phase 3: Activity
        activity_data = self._get_summarized_activity(default_branch)
        activity = RepoContextActivity(
            recent_commits=activity_data["recent_commits"],
            open_pull_requests=activity_data["open_pull_requests"],
            stats=RepoContextStats(**activity_data["stats"]),
        )

        # Phase 4: Readme
        readme_snippet = self._get_readme_snippet(default_branch)

        return RepoContextReport(
            target=self.executor.repo or "local",
            metadata=metadata,
            structure=structure,
            activity=activity,
            readme_snippet=readme_snippet,
        )

    def _get_readme_snippet(self, branch: str, limit: int = 2000) -> str | None:
        """
        Fetch and truncate README.md.
        """
        content = self.file_manager.get_file_content("README.md", ref=branch)
        if not content:
            return None

        # Normalize whitespace
        import re

        content = re.sub(r"\n{3,}", "\n\n", content).strip()

        return (
            (content[:limit] + "\n\n...[truncated]")
            if len(content) > limit
            else content
        )

    def _get_summarized_activity(self, branch: str) -> dict[str, Any]:
        """
        Fetch and format recent commits, PRs, and aggregate stats.
        """
        # 1. Fetch recent commits (limit 10)
        raw_commits = self.commits_manager.get_commits_for_analysis(
            branch=branch, limit=10
        )
        summarized_commits = [
            TraceCommit(
                sha=c.get("sha", ""),
                message=c.get("commit", {}).get("message", "").split("\n")[0],
                author=c.get("commit", {}).get("author", {}).get("name", "Unknown"),
                date=c.get("commit", {}).get("author", {}).get("date", ""),
                branch=branch,
                is_merge=len(c.get("parents", [])) > 1,
            )
            for c in raw_commits
        ]

        # 2. Fetch open PRs (limit 10)
        raw_prs = self.pr_manager.list_prs(state="open", limit=10)
        summarized_prs = []
        for pr in raw_prs:
            status = "Draft" if pr.get("draft") else "Open"
            summarized_prs.append(
                TracePR(
                    number=int(pr.get("number", 0)),
                    title=str(pr.get("title", "Untitled")),
                    author=pr.get("author", {}).get("login", "Unknown"),
                    status=status,
                    created_at=str(pr.get("createdAt", "")),
                    labels=[t.get("name") for t in pr.get("labels", [])]
                    if isinstance(pr.get("labels"), list)
                    else [],
                    draft=bool(pr.get("draft")),
                )
            )

        # 3. Calculate 7-day stats
        seven_days_ago = (datetime.now() - timedelta(days=7)).isoformat()
        recent_for_stats = self.commits_manager.get_commits_for_analysis(
            branch=branch, since=seven_days_ago, limit=100
        )

        active_contributors = {
            c.get("commit", {}).get("author", {}).get("email") for c in recent_for_stats
        }

        return {
            "recent_commits": summarized_commits,
            "open_pull_requests": summarized_prs,
            "stats": {
                "commits_last_7d": len(recent_for_stats),
                "open_prs_count": len(raw_prs),
                "active_contributors_last_7d": len(active_contributors),
            },
        }

    def _get_smart_structure(
        self, branch: str, max_depth: int = 2, max_per_level: int = 20
    ) -> list[dict[str, Any]]:
        """
        Get file structure with smart truncation and priority preservation.
        """
        raw_tree = self.repo_manager.get_file_structure(branch)
        if not raw_tree:
            return []

        # 1. Separate priority files (they always get in)
        priority_files = []
        other_files = []

        for item in raw_tree:
            path = item.get("path", "")
            item["priority"] = self._is_priority_file(path)

            if item["priority"]:
                priority_files.append(item)
            else:
                other_files.append(item)

        # 2. Filter non-priority files by depth and count
        filtered_structure = []

        # Group other files by their parent directory
        from collections import defaultdict

        levels = defaultdict(list)

        for item in other_files:
            path = item.get("path", "")
            depth = path.count("/") + 1
            levels[depth].append(item)

        # Apply limits
        for depth in sorted(levels.keys()):
            if depth > max_depth:
                # We don't add "truncated" markers for whole depths here
                # to avoid noise, but maybe we should?
                continue

            items = levels[depth]
            if len(items) > max_per_level:
                filtered_structure.extend(items[:max_per_level])
                filtered_structure.append(
                    {
                        "path": f"depth_{depth}_others",
                        "type": "truncated",
                        "count": len(items) - max_per_level,
                    }
                )
            else:
                filtered_structure.extend(items)

        # 3. Combine and return (ensure unique paths if priority overlapped)
        seen_paths = set()
        final_list = []

        for item in priority_files + filtered_structure:
            if item["path"] not in seen_paths:
                final_list.append(item)
                seen_paths.add(item["path"])

        # Sort by path for predictable output
        final_list.sort(key=lambda x: x["path"])
        return final_list

    def _is_priority_file(self, path: str) -> bool:
        """Check if file should always be included regardless of depth."""
        return any(pattern in path for pattern in self.PRIORITY_WHITELIST)
