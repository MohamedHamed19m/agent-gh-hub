from typing import Any, Dict, List, Optional

from pydantic import BaseModel


class FileMatch(BaseModel):
    path: str
    match_snippet: Optional[str] = None


class TraceCommit(BaseModel):
    sha: str
    message: str
    author: str
    date: str
    branch: str
    is_merge: bool = False


class TracePR(BaseModel):
    number: int
    title: str
    author: str
    status: str
    created_at: str
    labels: List[str] = []
    draft: bool = False


class FeatureTrace(BaseModel):
    keyword: str
    repo: str
    file_matches: List[FileMatch] = []
    commit_matches: List[TraceCommit] = []
    pr_matches: List[TracePR] = []
    contributors: List[Dict[str, Any]] = []
    total_mentions: int = 0
    first_mention_date: Optional[str] = None
    last_activity_date: Optional[str] = None


class MultiRepoFeatureTrace(BaseModel):
    keyword: str
    repos_searched: List[str]
    traces: Dict[str, FeatureTrace]
