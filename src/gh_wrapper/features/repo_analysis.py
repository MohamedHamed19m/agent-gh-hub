import logging
from typing import Dict, List

from ..commands.commits import CommitsManager
from ..models.analysis import (
    CommitAnalysisReport,
    ContributorStats,
    DailyStats,
    TimePatterns,
)

logger = logging.getLogger(__name__)


class RepoAnalyzer:
    """Feature layer for repository analysis and insights"""

    def __init__(self, commits_manager: CommitsManager):
        self.commits_manager = commits_manager

    def analyze_commit_patterns(
        self, branches: List[str], days_back: int = 30
    ) -> CommitAnalysisReport:
        """
        Orchestrates commit pattern analysis across multiple branches
        """
        raise NotImplementedError()

    def format_as_markdown(self, report: CommitAnalysisReport) -> str:
        """
        Formats the analysis report as a human-readable Markdown string
        """
        raise NotImplementedError()

    def _calculate_daily_trend(self, all_commits: List[Dict]) -> List[DailyStats]:
        """Helper to calculate daily commit counts"""
        raise NotImplementedError()

    def _analyze_contributors(self, all_commits: List[Dict]) -> List[ContributorStats]:
        """Helper to analyze contributor activity"""
        raise NotImplementedError()

    def _analyze_time_patterns(self, all_commits: List[Dict]) -> TimePatterns:
        """Helper to analyze hourly and weekday patterns"""
        raise NotImplementedError()
