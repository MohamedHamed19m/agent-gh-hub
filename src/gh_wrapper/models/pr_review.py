from typing import Dict, List, Literal, Optional

from pydantic import BaseModel


class Location(BaseModel):
    file_path: str
    line_number: int


class FileModification(BaseModel):
    file_path: str
    status: Literal["added", "removed", "modified"]


class PrSummary(BaseModel):
    modified_files: List[FileModification]
    key_diffs: Dict[str, str]  # File path to a concise diff summary


class SuggestedComment(BaseModel):
    text: str
    severity: Literal["suggestion", "warning", "error"]
    location: Location
    comment_type: str  # e.g., "coding_standard", "potential_bug"


class PrReviewOutput(BaseModel):
    input_params: "PrReviewInput"  # Forward reference to PrReviewInput
    summary: PrSummary
    suggested_comments: List[SuggestedComment]
    metrics: Dict[str, int]  # e.g., {"lines_added": 100, "lines_deleted": 50}


class PrReviewInput(BaseModel):
    repo_name: str
    pr_id: int
    target_branch: Optional[str] = None
    review_depth: Optional[str] = None
