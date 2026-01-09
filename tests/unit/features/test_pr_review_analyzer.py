import pytest

from gh_wrapper.commands.pull_requests import PRManager
from gh_wrapper.features.pr_review_analyzer import PrReviewAnalyzer
from gh_wrapper.models.pr_review import (
    FileModification,
    Location,
    PrReviewInput,
    PrReviewOutput,
    PrSummary,
    SuggestedComment,
)


# Mock PRManager for unit tests
@pytest.fixture
def mock_pr_manager(mocker) -> PRManager:
    return mocker.Mock(spec=PRManager)


# --- Tests for analyze_pr method ---


def test_analyze_pr_with_diff(mock_pr_manager: PRManager):
    """Test analyze_pr method with a mock PR diff."""
    pr_manager = mock_pr_manager

    # Mock PRManager.get_pr_diff to return a sample diff string
    sample_diff = """diff --git a/file1.py b/file1.py
index abcdefg..hijklmn 100644
--- a/file1.py
+++ b/file1.py
@@ -1,3 +1,4 @@
def my_func():
-    print("hello")
+    print("hello world")
+    # new comment
@@ -5,3 +6,8 @@
def another_func():
    pass
+
+def added_func():
+    print("This is a new function")
+
"""
    pr_manager.get_pr_diff.return_value = sample_diff

    analyzer = PrReviewAnalyzer(pr_manager=pr_manager)
    # Using a dummy input, actual values will be mocked by PRManager.
    # The content of pr_diff_patch from get_pr_diff is what matters here.
    review_output = analyzer.analyze_pr(
        pr_input=PrReviewInput(
            repo_name="owner/repo",
            pr_id=1,
            target_branch=None,
            review_depth="full",
        )
    )

    assert isinstance(review_output, PrReviewOutput)
    assert review_output.input_params.pr_id == 1
    assert review_output.summary.modified_files == [
        FileModification(file_path="file1.py", status="modified")
    ]
    assert review_output.metrics["lines_added"] == 6
    assert review_output.metrics["lines_deleted"] == 1

    # Check that get_pr_diff was called
    pr_manager.get_pr_diff.assert_called_once_with(1)


def test_analyze_pr_with_target_branch(mock_pr_manager: PRManager):
    """Test analyze_pr method with a target branch."""
    pr_manager = mock_pr_manager

    # Mock PRManager.get_pr_diff_against_branch to return a sample diff string
    sample_diff = """diff --git a/file1.py b/file1.py
index abcdefg..hijklmn 100644
--- a/file1.py
+++ b/file1.py
@@ -1,3 +1,4 @@
def my_func():
-    print("hello")
+    print("hello world")
+    # new comment
"""
    pr_manager.get_pr_diff_against_branch.return_value = sample_diff

    analyzer = PrReviewAnalyzer(pr_manager=pr_manager)
    analyzer.analyze_pr(
        pr_input=PrReviewInput(
            repo_name="owner/repo",
            pr_id=2,
            target_branch="develop",
            review_depth="full",
        )
    )

    pr_manager.get_pr_diff_against_branch.assert_called_once_with(2, "develop")


# --- Tests for format_as_markdown method ---


def test_format_as_markdown_empty_output(mock_pr_manager):
    """Test format_as_markdown with an empty review output."""
    pr_output = PrReviewOutput(
        input_params=PrReviewInput(repo_name="owner/repo", pr_id=1),
        summary=PrSummary(modified_files=[], key_diffs={}),
        suggested_comments=[],
        metrics={"lines_added": 0, "lines_deleted": 0, "files_changed": 0},
    )

    analyzer = PrReviewAnalyzer(pr_manager=mock_pr_manager)
    markdown = analyzer.format_as_markdown(pr_output)

    expected_markdown = (
        "# PR Review for owner/repo#1\n\n## Summary\n\n"
        "No files were modified in this PR.\n\n## Suggested Comments\n\n"
        "No suggestions or potential issues found.\n\n## Metrics\n\n"
        "- Lines added: 0\n- Lines deleted: 0\n- Files changed: 0\n\n"
    )
    assert markdown == expected_markdown


def test_format_as_markdown_with_content(mock_pr_manager):
    """Test format_as_markdown with populated review output."""
    pr_output = PrReviewOutput(
        input_params=PrReviewInput(
            repo_name="owner/repo", pr_id=1, target_branch="main", review_depth="full"
        ),
        summary=PrSummary(
            modified_files=[
                FileModification(file_path="src/main.py", status="modified"),
                FileModification(file_path="tests/test.py", status="added"),
            ],
            key_diffs={"src/main.py": "..."},
        ),
        suggested_comments=[
            SuggestedComment(
                text="Consider adding type hints here.",
                severity="suggestion",
                location=Location(file_path="src/main.py", line_number=50),
                comment_type="coding_standard",
            ),
            SuggestedComment(
                text="This might be an unhandled exception.",
                severity="warning",
                location=Location(file_path="src/main.py", line_number=75),
                comment_type="potential_bug",
            ),
        ],
        metrics={"lines_added": 100, "lines_deleted": 50, "files_changed": 2},
    )

    analyzer = PrReviewAnalyzer(pr_manager=mock_pr_manager)
    markdown = analyzer.format_as_markdown(pr_output)

    expected_markdown = (
        "# PR Review for owner/repo#1\n\n## Summary\n\n"
        "### Modified Files:\n- `src/main.py` (modified)\n- `tests/test.py` (added)\n\n"
        "### Key Diffs:\n- **src/main.py**: ... (diff details)\n\n"
        "## Suggested Comments\n\n**[Suggestion]** [coding_standard] "
        "(src/main.py:50):\n> Consider adding type hints here.\n\n"
        "**[Warning]** [potential_bug] (src/main.py:75):\n"
        "> This might be an unhandled exception.\n\n## Metrics\n\n"
        "- Lines added: 100\n- Lines deleted: 50\n- Files changed: 2\n\n"
    )
    assert markdown == expected_markdown
