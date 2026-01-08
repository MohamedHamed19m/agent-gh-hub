"""
Integration tests using a dedicated test branch with known content.
This allows you to verify actual functionality without mocking.
"""

import pytest

from gh_wrapper.commands.commits import CommitsManager
from gh_wrapper.commands.files import FileManager
from gh_wrapper.core.executor import GHExecutor
from gh_wrapper.features.repo_context import RepoContextAnalyzer
from gh_wrapper.features.user_tracer import UserTracer

# Configuration for test branch
TEST_REPO = "MohamedHamed19m/agent-gh-hub"
TEST_BRANCH = "test-branch-fixture"  # Dedicated branch for testing
TEST_FILES = {
    "test-file-1.txt": "Hello from test file 1",
    "test-file-2.py": 'print("Test file 2")',
    "test-dir/nested-file.md": "# Nested Test File",
}


class TestWithKnownBranch:
    """Tests that use a dedicated branch with known content."""

    @pytest.fixture(scope="class")
    def executor(self) -> GHExecutor:
        """Initialize executor for test branch."""
        return GHExecutor(repo=TEST_REPO, use_cache=False)

    def test_read_specific_file(self, executor: GHExecutor) -> None:
        """Test reading a specific file from test branch."""
        file_manager = FileManager(executor)

        # Read known test file
        content = file_manager.get_file_content("test-file-1.txt", ref=TEST_BRANCH)

        # Assert expected content
        assert content is not None, "File content should not be None"
        assert (
            "Hello from test file 1" in content
        ), f"Expected content not found. Got: {content}"
        print(f"✓ File read successful: {content}")

    def test_read_all_test_files(self, executor: GHExecutor) -> None:
        """Test reading multiple known test files."""
        file_manager = FileManager(executor)

        for file_path, expected_content in TEST_FILES.items():
            try:
                content = file_manager.get_file_content(file_path, ref=TEST_BRANCH)
                assert (
                    expected_content in content
                ), f"File {file_path}: expected '{expected_content}' not found"
                print(f"✓ {file_path}: Content verified")
            except Exception as e:
                print(f"✗ {file_path}: {e}")
                raise

    def test_repo_context_from_test_branch(self, executor: GHExecutor) -> None:
        """Test repo context analysis on test branch."""
        analyzer = RepoContextAnalyzer(executor)

        # Analyze context (works on current branch of executor)
        context = analyzer.analyze_current_context()

        # Assert context structure
        assert context is not None, "Context should not be None"
        assert "structure" in context, "Context should have 'structure' key"
        assert "metadata" in context, "Context should have 'metadata' key"

        structure = context.get("structure", [])
        assert len(structure) > 0, "Structure should not be empty"

        print(f"✓ Found {len(structure)} items in repo structure")
        print(f"✓ Metadata: {context.get('metadata', {})}")

    def test_file_structure_contains_test_files(self, executor: GHExecutor) -> None:
        """Test that file structure includes our known test files."""
        analyzer = RepoContextAnalyzer(executor)
        context = analyzer.analyze_current_context(branch=TEST_BRANCH)

        structure = context.get("structure", [])
        found_files = {item["path"] for item in structure}

        # Check for at least some of our test files
        for test_file in TEST_FILES.keys():
            assert (
                test_file in found_files
            ), f"Test file '{test_file}' not found in structure. Found: {found_files}"
            print(f"✓ Found test file in structure: {test_file}")

    def test_commit_history_on_test_branch(self, executor: GHExecutor) -> None:
        """Test reading commit history from test branch."""
        commits_manager = CommitsManager(executor)

        # Get recent commits from test branch
        commits = commits_manager.list_commits(branch=TEST_BRANCH, limit=5)

        assert commits is not None, "Commits should not be None"
        assert len(commits) > 0, "Should have at least one commit"

        for commit in commits:
            assert "sha" in commit, "Commit should have 'sha'"
            assert "message" in commit, "Commit should have 'message'"
            print(f"✓ Commit: {commit['sha'][:7]} - {commit['message']}")

    def test_user_activity_on_test_branch(self, executor: GHExecutor) -> None:
        """Test tracing user activity on test branch."""
        user_tracer = UserTracer(executor)

        # Trace activity from a known user
        recent_work = user_tracer.trace_recent_work(
            username="MohamedHamed19m", repo=TEST_REPO, limit=5, branch=TEST_BRANCH
        )

        assert recent_work is not None, "Recent work should not be None"

        if recent_work:
            for commit in recent_work:
                assert "sha" in commit, "Should have commit SHA"
                assert "message" in commit, "Should have commit message"
                print(f"✓ User commit: {commit['message']}")
        else:
            print("⚠ No commits found for user on test branch")


class TestExpectedValues:
    """Tests that verify specific expected values."""

    @pytest.fixture
    def executor(self) -> GHExecutor:
        """Initialize executor for test branch."""
        return GHExecutor(repo=TEST_REPO, use_cache=False)

    def test_test_file_1_exact_content(self, executor: GHExecutor) -> None:
        """Verify exact content of test-file-1.txt."""
        file_manager = FileManager(executor)
        content = file_manager.get_file_content("test-file-1.txt", ref=TEST_BRANCH)

        # Handle BOM if present
        content_clean = content.lstrip("\ufeff").strip()
        expected = TEST_FILES["test-file-1.txt"].strip()

        assert (
            content_clean == expected
        ), f"Expected:\n{expected}\n\nGot:\n{content_clean}"

    def test_python_file_is_valid_python(self, executor: GHExecutor) -> None:
        """Verify test Python file is syntactically valid."""
        file_manager = FileManager(executor)
        content = file_manager.get_file_content("test-file-2.py", ref=TEST_BRANCH)

        # Try to compile it
        try:
            compile(content, "test-file-2.py", "exec")
            print("✓ Python file is syntactically valid")
        except SyntaxError as e:
            pytest.fail(f"Python file has syntax error: {e}")


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])
