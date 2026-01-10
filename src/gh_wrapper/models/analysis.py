from typing import Dict, List, Optional

from pydantic import BaseModel, Field

from .trace import TraceCommit, TracePR


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


class RepoContextMetadata(BaseModel):
    default_branch: str
    description: Optional[str] = None
    latest_release: Optional[str] = None
    stars: Optional[int] = 0
    forks: Optional[int] = 0
    is_fork: bool = False
    is_archived: bool = False
    topics: List[str] = []


class RepoContextStructureItem(BaseModel):
    path: str
    type: str
    sha: Optional[str] = None
    priority: bool = False
    count: Optional[int] = None  # For truncated items


class RepoContextStats(BaseModel):
    commits_last_7d: int
    open_prs_count: int
    active_contributors_last_7d: int


class RepoContextActivity(BaseModel):
    recent_commits: List[TraceCommit] = []
    open_pull_requests: List[TracePR] = []
    stats: RepoContextStats


class RepoContextReport(BaseModel):
    target: str
    metadata: RepoContextMetadata
    structure: List[RepoContextStructureItem]
    activity: RepoContextActivity
    readme_snippet: Optional[str] = None
