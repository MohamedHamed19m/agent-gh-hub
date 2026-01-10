import logging
from collections import Counter
from datetime import datetime, timedelta
from typing import Any

from ..commands.commits import CommitsManager
from ..models.analysis import (
    CommitAnalysisReport,
    ContributorStats,
    DailyStats,
    TimePatterns,
)

logger = logging.getLogger(__name__)


class RepoAnalyzer:
    """Feature layer for repository analysis and insights.

    This class orchestrates complex logic by fetching raw commit data via CommitsManager
    and transforming it into structured insights and human-readable reports.

    Example:
        >>> analyzer = RepoAnalyzer(commits_manager)
        >>> report = analyzer.analyze_commit_patterns(["main"], days_back=30)
        >>> print(analyzer.format_as_markdown(report))

    """

    def __init__(self, commits_manager: CommitsManager):
        """Initialize the RepoAnalyzer.

        Args:
            commits_manager: An instance of CommitsManager to fetch commit data.

        """
        self.commits_manager = commits_manager

    def analyze_commit_patterns(
        self, branches: list[str], days_back: int = 30
    ) -> CommitAnalysisReport:
        """Orchestrates commit pattern analysis across multiple branches.

        Args:
            branches: A list of branch names to analyze.
            days_back: Number of days to look back for commits. Defaults to 30.

        Returns:
            A CommitAnalysisReport Pydantic model containing the aggregated insights.

        Raises:
            ValueError: If branches list is empty or days_back is not positive.

        """
        if not branches:
            raise ValueError("At least one branch must be provided.")
        if days_back <= 0:
            raise ValueError("days_back must be a positive integer.")

        since = (datetime.now() - timedelta(days=days_back)).isoformat()

        all_commits: list[dict[str, Any]] = []
        seen_shas = set()

        for branch in branches:
            try:
                commits = self.commits_manager.get_commits_for_analysis(
                    branch=branch, since=since
                )
                for c in commits:
                    sha = c.get("sha")
                    if sha and sha not in seen_shas:
                        all_commits.append(c)
                        seen_shas.add(sha)
            except Exception as e:
                logger.warning(f"Failed to fetch commits for branch {branch}: {e}")

        all_commits.sort(
            key=lambda x: x.get("commit", {}).get("author", {}).get("date", ""),
            reverse=True,
        )

        return CommitAnalysisReport(
            repository=self.commits_manager.executor.repo or "unknown",
            branches=branches,
            since=since,
            total_commits=len(all_commits),
            daily_trends=self._calculate_daily_trend(all_commits),
            contributors=self._analyze_contributors(all_commits),
            time_patterns=self._analyze_time_patterns(all_commits),
        )

    def format_as_markdown(self, report: CommitAnalysisReport) -> str:
        """Formats the analysis report as a human-readable Markdown string"""
        lines = [
            "# Repository Analysis Report",
            f"**Repository:** {report.repository}",
            f"**Branches:** {', '.join(report.branches)}",
            f"**Since:** {report.since}",
            f"**Total Commits:** {report.total_commits}",
            "",
            "## Contributor Activity",
            "| Author | Commits | Percentage |",
            "| :--- | :--- | :--- |",
        ]

        for c in report.contributors:
            lines.append(f"| {c.author} | {c.commit_count} | {c.percentage}% |")

        lines.extend(
            [
                "",
                "## Daily Trends",
                "| Date | Commit Count |",
                "| :--- | :--- |",
            ]
        )

        for d in report.daily_trends:
            lines.append(f"| {d.date} | {d.commit_count} |")

        lines.extend(
            [
                "",
                "## Time-based Patterns",
                "",
                "### Weekly Distribution",
                "| Day | Commits |",
                "| :--- | :--- |",
            ]
        )

        for day, count in report.time_patterns.weekday_distribution.items():
            lines.append(f"| {day} | {count} |")

        lines.extend(
            [
                "",
                "### Hourly Distribution (Peak Hours)",
                "| Hour | Commits |",
                "| :--- | :--- |",
            ]
        )

        # Only show hours with commits to keep it concise, or maybe all?
        # Let's show all for now or top 5? Let's show hours with > 0 commits.
        for hour, count in sorted(report.time_patterns.hourly_distribution.items()):
            if count > 0:
                lines.append(f"| {hour:02d}:00 | {count} |")

        return "\n".join(lines)

    def _calculate_daily_trend(
        self, all_commits: list[dict[str, Any]]
    ) -> list[DailyStats]:
        """Helper to calculate daily commit counts"""
        date_counts: Counter[str] = Counter()
        for c in all_commits:
            date_str = c.get("commit", {}).get("author", {}).get("date", "")
            if date_str:
                # ISO date is YYYY-MM-DDTHH:MM:SSZ
                day = date_str.split("T")[0]
                date_counts[day] += 1

        # Sort by date
        sorted_dates = sorted(date_counts.keys())
        return [DailyStats(date=d, commit_count=date_counts[d]) for d in sorted_dates]

    def _analyze_contributors(
        self, all_commits: list[dict[str, Any]]
    ) -> list[ContributorStats]:
        """Helper to analyze contributor activity"""
        author_counts: Counter[str] = Counter()
        for c in all_commits:
            author = c.get("commit", {}).get("author", {}).get("name", "Unknown")
            author_counts[author] += 1

        total = len(all_commits)
        stats = []
        for author, count in author_counts.most_common():
            stats.append(
                ContributorStats(
                    author=author,
                    commit_count=count,
                    percentage=round((count / total * 100), 2) if total > 0 else 0,
                )
            )
        return stats

    def _analyze_time_patterns(self, all_commits: list[dict[str, Any]]) -> TimePatterns:
        """Helper to analyze hourly and weekday patterns"""
        hour_counts: Counter[int] = Counter()
        weekday_counts: Counter[str] = Counter()

        for c in all_commits:
            date_str = c.get("commit", {}).get("author", {}).get("date", "")
            if date_str:
                try:
                    # Handle both Z and +HH:MM offsets if present,
                    # but simple split/parse is often enough for GH API ISO dates
                    dt = datetime.fromisoformat(date_str.replace("Z", "+00:00"))
                    hour_counts[dt.hour] += 1
                    weekday_counts[dt.strftime("%A")] += 1
                except ValueError:
                    continue

        # Ensure all hours (0-23) are present for consistency
        hourly = {h: hour_counts.get(h, 0) for h in range(24)}

        weekdays = [
            "Monday",
            "Tuesday",
            "Wednesday",
            "Thursday",
            "Friday",
            "Saturday",
            "Sunday",
        ]
        daily = {d: weekday_counts.get(d, 0) for d in weekdays}

        return TimePatterns(hourly_distribution=hourly, weekday_distribution=daily)
