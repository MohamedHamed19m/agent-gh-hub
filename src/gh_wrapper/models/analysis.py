from typing import Dict, List

from pydantic import BaseModel, Field


class ContributorStats(BaseModel):
    author: str
    commit_count: int
    percentage: float


class DailyStats(BaseModel):
    date: str
    commit_count: int


class TimePatterns(BaseModel):
    hourly_distribution: Dict[int, int] = Field(
        description="Hour (0-23) to commit count"
    )

    weekday_distribution: Dict[str, int] = Field(
        description="Day of week to commit count"
    )


class CommitAnalysisReport(BaseModel):
    repository: str
    branches: List[str]
    since: str
    total_commits: int
    daily_trends: List[DailyStats]
    contributors: List[ContributorStats]
    time_patterns: TimePatterns
