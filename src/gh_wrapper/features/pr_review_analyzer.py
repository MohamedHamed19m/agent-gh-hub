import re
from typing import Dict, List

from src.gh_wrapper.commands.pull_requests import PRManager
from src.gh_wrapper.models.pr_review import (
    FileModification,
    PrReviewInput,
    PrReviewOutput,
    PrSummary,
    SuggestedComment,
)


class PrReviewAnalyzer:
    def __init__(
        self,
        pr_manager: PRManager,
    ):
        self.pr_manager = pr_manager

    def analyze_pr(self, pr_input: PrReviewInput) -> PrReviewOutput:
        """
        Analyzes a Pull Request to generate a summary and suggested comments.
        """
        # Fetch raw PR data including diffs
        if pr_input.target_branch:
            pr_diff_patch = self.pr_manager.get_pr_diff_against_branch(
                pr_input.pr_id, pr_input.target_branch
            )
        else:
            pr_diff_patch = self.pr_manager.get_pr_diff(pr_input.pr_id)

        # --- Diff Parsing Logic ---
        summary_data = PrSummary(modified_files=[], key_diffs={})
        suggested_comments_data: List[SuggestedComment] = []
        metrics_data: Dict[str, int] = {
            "lines_added": 0,
            "lines_deleted": 0,
            "files_changed": 0,
        }

        current_file_path = None
        current_file_status = None
        lines_added_count = 0
        lines_deleted_count = 0

        # Regex to find file diff headers and statuses
        diff_header_pattern = re.compile(r"^diff --git a/(.*) b/.*")
        new_file_pattern = re.compile(r"^new file mode ")
        deleted_file_pattern = re.compile(r"^deleted file mode ")
        # Matches lines starting with '+' or '-'
        diff_line_pattern = re.compile(r"^[+-]")

        for line in pr_diff_patch.splitlines():
            if line.startswith("diff --git"):
                # Process the previous file's data before starting a new one
                if current_file_path and current_file_status:
                    summary_data.modified_files.append(
                        FileModification(
                            file_path=current_file_path, status=current_file_status
                        )
                    )
                    metrics_data["files_changed"] += 1

                # Extract the file path from the diff header
                match = diff_header_pattern.match(line)
                if match:
                    current_file_path = match.group(1)
                    current_file_status = "modified"  # Default status
                else:
                    current_file_path = None  # Malformed header, skip file
                    current_file_status = None
            elif current_file_path:
                if new_file_pattern.match(line):
                    current_file_status = "added"
                elif deleted_file_pattern.match(line):
                    current_file_status = "removed"
                # Count lines starting with '+' or '-' for metrics
                elif diff_line_pattern.match(line):
                    if line.startswith("+++ ") or line.startswith("--- "):
                        continue
                    if line.startswith("+"):
                        lines_added_count += 1
                    elif line.startswith("-"):
                        lines_deleted_count += 1

        # Add the last file processed if it exists and has a determined status
        if current_file_path and current_file_status:
            summary_data.modified_files.append(
                FileModification(
                    file_path=current_file_path, status=current_file_status
                )
            )
            metrics_data["files_changed"] += 1

        metrics_data["lines_added"] = lines_added_count
        metrics_data["lines_deleted"] = lines_deleted_count
        # --- End of basic diff parsing logic ---

        return PrReviewOutput(
            input_params=pr_input,
            summary=summary_data,
            suggested_comments=suggested_comments_data,
            metrics=metrics_data,
        )

    def format_as_markdown(self, pr_review_output: PrReviewOutput) -> str:
        """
        Formats the PR review output into a human-readable Markdown string.
        """
        params = pr_review_output.input_params
        markdown_output = f"# PR Review for {params.repo_name}#{params.pr_id}\n\n"

        # Summary Section
        markdown_output += "## Summary\n\n"
        if not pr_review_output.summary.modified_files:
            markdown_output += "No files were modified in this PR.\n\n"
        else:
            markdown_output += "### Modified Files:\n"
            for file_mod in pr_review_output.summary.modified_files:
                markdown_output += f"- `{file_mod.file_path}` ({file_mod.status})\n"
            markdown_output += "\n"

        if pr_review_output.summary.key_diffs:
            markdown_output += "### Key Diffs:\n"
            for file_path, _ in pr_review_output.summary.key_diffs.items():
                markdown_output += f"- **{file_path}**: ... (diff details)\n"
            markdown_output += "\n"

        # Suggested Comments Section
        markdown_output += "## Suggested Comments\n\n"
        if not pr_review_output.suggested_comments:
            markdown_output += "No suggestions or potential issues found.\n\n"
        else:
            for comment in pr_review_output.suggested_comments:
                markdown_output += (
                    f"**[{comment.severity.capitalize()}]** [{comment.comment_type}] "
                    f"({comment.location.file_path}:{comment.location.line_number}):\n"
                )
                markdown_output += f"> {comment.text}\n\n"

        # Metrics Section
        markdown_output += "## Metrics\n\n"
        for key, value in pr_review_output.metrics.items():
            markdown_output += f"- {key.replace('_', ' ').capitalize()}: {value}\n"
        markdown_output += "\n"

        return markdown_output
