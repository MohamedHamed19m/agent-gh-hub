# Testing Guide

## Overview

This project follows a **Test-Driven Development (TDD)** approach with clear separation between unit and integration tests. All code should achieve **>80% unit test coverage** while integration tests verify real-world functionality.

---

## Testing Philosophy

### The Testing Pyramid

```
         /\
        /  \  Integration Tests (Real GitHub API)
       /____\  - Verify end-to-end functionality
      /      \ - Test against public repos
     /________\ - Excluded from coverage stats
    /          \
   /   Unit     \ Unit Tests (Mocked)
  /    Tests     \ - Test logic in isolation
 /________________\ - Mock all external dependencies
                    - Target: >80% coverage
```

### Test Types

#### Unit Tests
- **Purpose:** Verify logic in isolation
- **Location:** `tests/unit/`
- **Dependencies:** All external calls mocked (GHExecutor, managers)
- **Coverage:** >80% required
- **Speed:** Fast (<1 second per test)

#### Integration Tests
- **Purpose:** Verify interaction with real GitHub CLI/API
- **Location:** `tests/integration/`
- **Dependencies:** Real `gh` CLI, requires authentication
- **Coverage:** Excluded from stats
- **Speed:** Slower (network calls)

---

## Running Tests

### Basic Commands

```bash
# Run all unit tests with coverage
uv run pytest tests/unit --cov=src/gh_wrapper --cov-report=term-missing

# Run specific test file
uv run pytest tests/unit/features/test_feature_tracer.py -v

# Run specific test
uv run pytest tests/unit/features/test_feature_tracer.py::TestFeatureTracer::test_trace_single_repo -v

# Run with verbose output
uv run pytest tests/unit -v

# Run integration tests
export RUN_INTEGRATION_TESTS=1
uv run pytest tests/integration -v
```

### Coverage Reports

```bash
# Terminal coverage report
uv run pytest tests/unit --cov=src/gh_wrapper --cov-report=term-missing

# HTML coverage report
uv run pytest tests/unit --cov=src/gh_wrapper --cov-report=html
# Open htmlcov/index.html in browser

# Check specific module coverage
uv run pytest tests/unit --cov=src/gh_wrapper/features/feature_tracer --cov-report=term-missing
```

### Watch Mode (Development)

```bash
# Re-run tests on file changes (requires pytest-watch)
uv run ptw tests/unit -- --cov=src/gh_wrapper
```

---

## Unit Testing Patterns

### Pattern 1: Testing Commands (Mocking GHExecutor)

#### Setup
```python
# tests/unit/commands/test_repository.py

import pytest
import json
from unittest.mock import Mock
from gh_wrapper.commands.repository import RepoManager
from gh_wrapper.core.exceptions import GHCommandError


class TestRepoManager:
    """Test RepoManager command methods"""
    
    @pytest.fixture
    def mock_executor(self):
        """Mock GHExecutor for testing"""
        executor = Mock()
        executor.repo = "owner/repo"
        return executor
    
    @pytest.fixture
    def repo_manager(self, mock_executor):
        """RepoManager instance with mocked executor"""
        return RepoManager(mock_executor)
```

#### Testing Successful Calls
```python
def test_list_branches_success(self, repo_manager, mock_executor):
    """Test successful branch listing"""
    # Arrange: Mock the GitHub CLI response
    mock_data = [
        {"name": "main", "commit": {"sha": "abc123"}},
        {"name": "develop", "commit": {"sha": "def456"}}
    ]
    mock_executor.execute.return_value = json.dumps(mock_data)
    
    # Act: Call the method
    result = repo_manager.list_branches()
    
    # Assert: Verify results
    assert len(result) == 2
    assert result[0]["name"] == "main"
    assert result[1]["name"] == "develop"
    
    # Verify gh command was called correctly
    mock_executor.execute.assert_called_once()
    call_args = mock_executor.execute.call_args[0][0]
    assert "gh" in call_args
    assert "api" in call_args
```

#### Testing Error Handling
```python
def test_list_branches_error(self, repo_manager, mock_executor):
    """Test error handling when gh command fails"""
    # Arrange: Mock command failure
    mock_executor.execute.side_effect = GHCommandError(
        "API rate limit exceeded",
        exit_code=1
    )
    
    # Act & Assert: Verify exception is raised
    with pytest.raises(GHCommandError) as exc_info:
        repo_manager.list_branches()
    
    assert "rate limit" in str(exc_info.value)
```

#### Testing Command Structure
```python
def test_get_commits_command_structure(self, repo_manager, mock_executor):
    """Verify correct gh CLI command is constructed"""
    mock_executor.execute.return_value = "[]"
    
    # Call with parameters
    repo_manager.get_commits(
        branch="main",
        limit=10,
        since="2024-01-01"
    )
    
    # Verify command structure
    call_args = mock_executor.execute.call_args[0][0]
    assert call_args[0] == "gh"
    assert call_args[1] == "api"
    assert "since=2024-01-01" in str(call_args)
    assert "per_page=10" in str(call_args)
```

---

### Pattern 2: Testing Features (Mocking Managers)

#### Setup with Multiple Mocks
```python
# tests/unit/features/test_feature_tracer.py

import pytest
from unittest.mock import Mock, patch
from datetime import datetime

from gh_wrapper.features.feature_tracer import FeatureTracer
from gh_wrapper.models.trace import FeatureTrace, MultiRepoFeatureTrace


class TestFeatureTracer:
    """Test FeatureTracer functionality"""
    
    @pytest.fixture
    def tracer(self):
        """FeatureTracer instance"""
        return FeatureTracer()
    
    @pytest.fixture
    def mock_managers(self):
        """Mock all command managers"""
        return {
            "file": Mock(),
            "commits": Mock(),
            "pr": Mock()
        }
```

#### Testing with Patched Imports
```python
@patch("gh_wrapper.features.feature_tracer.FileManager")
@patch("gh_wrapper.features.feature_tracer.CommitsManager")
@patch("gh_wrapper.features.feature_tracer.PRManager")
def test_trace_feature_composes_managers(
    self,
    mock_pr_class,
    mock_commits_class,
    mock_file_class,
    tracer
):
    """Test that trace_feature creates and uses managers correctly"""
    # Arrange: Setup mock manager instances
    mock_file_mgr = Mock()
    mock_commits_mgr = Mock()
    mock_pr_mgr = Mock()
    
    mock_file_class.return_value = mock_file_mgr
    mock_commits_class.return_value = mock_commits_mgr
    mock_pr_class.return_value = mock_pr_mgr
    
    # Mock manager responses
    mock_file_mgr.search_in_files.return_value = []
    mock_commits_mgr.get_commits.return_value = []
    mock_pr_mgr.list_prs.return_value = []
    
    # Act: Execute trace
    result = tracer.trace_feature(
        keyword="test",
        repos="org/repo"
    )
    
    # Assert: Verify managers were created with correct repo
    mock_file_class.assert_called_once_with("org/repo")
    mock_commits_class.assert_called_once_with("org/repo")
    mock_pr_class.assert_called_once_with("org/repo")
    
    # Verify managers were called
    mock_file_mgr.search_in_files.assert_called()
    mock_commits_mgr.get_commits.assert_called()
    mock_pr_mgr.list_prs.assert_called()
```

#### Testing Aggregation Logic
```python
def test_contributor_aggregation(self, tracer):
    """Test contributor statistics calculation"""
    # Arrange: Sample commits and PRs
    commits = [
        TraceCommit(sha="1", message="msg", author="alice", date=datetime.now()),
        TraceCommit(sha="2", message="msg", author="alice", date=datetime.now()),
        TraceCommit(sha="3", message="msg", author="bob", date=datetime.now())
    ]
    prs = [
        TracePR(number=1, title="PR", author="alice", state="open", created_at=datetime.now()),
        TracePR(number=2, title="PR", author="charlie", state="closed", created_at=datetime.now())
    ]
    
    # Act: Aggregate contributors
    result = tracer._analyze_contributors(commits, prs)
    
    # Assert: Verify correct aggregation
    assert len(result) == 3
    
    # Alice should be first (2 commits + 1 PR = 3 total)
    assert result[0]["username"] == "alice"
    assert result[0]["commit_count"] == 2
    assert result[0]["pr_count"] == 1
    
    # Bob second (1 commit)
    assert result[1]["username"] == "bob"
    assert result[1]["commit_count"] == 1
    assert result[1]["pr_count"] == 0
```

#### Testing with Parametrize
```python
@pytest.mark.parametrize("repos_input,expected_count", [
    ("org/repo", 1),  # Single string
    (["org/repo1", "org/repo2"], 2),  # List
    (["org/repo1", "org/repo2", "org/repo3"], 3),  # Multiple
])
def test_repos_normalization(self, tracer, repos_input, expected_count):
    """Test repos parameter normalization with various inputs"""
    with patch.object(tracer, '_trace_single_repo') as mock_trace:
        mock_trace.return_value = FeatureTrace(
            keyword="test",
            repo="dummy",
            total_mentions=0
        )
        
        result = tracer.trace_feature("test", repos=repos_input)
        
        assert len(result.repos_searched) == expected_count
        assert mock_trace.call_count == expected_count
```

---

### Pattern 3: Testing Pydantic Models

```python
# tests/unit/models/test_trace.py

import pytest
from datetime import datetime
from pydantic import ValidationError
from gh_wrapper.models.trace import FileMatch, TraceCommit, FeatureTrace


class TestTraceModels:
    """Test Pydantic model validation and serialization"""
    
    def test_file_match_valid(self):
        """Test FileMatch creation with valid data"""
        match = FileMatch(
            path="src/main.py",
            line_count=5,
            snippets=["line 1", "line 2"]
        )
        
        assert match.path == "src/main.py"
        assert match.line_count == 5
        assert len(match.snippets) == 2
    
    def test_file_match_validation_error(self):
        """Test FileMatch validation on invalid data"""
        with pytest.raises(ValidationError) as exc_info:
            FileMatch(
                path="src/main.py",
                line_count="invalid",  # Should be int
                snippets=[]
            )
        
        errors = exc_info.value.errors()
        assert any("line_count" in str(e) for e in errors)
    
    def test_trace_commit_serialization(self):
        """Test TraceCommit can serialize to JSON"""
        commit = TraceCommit(
            sha="abc123",
            message="Test commit",
            author="dev-user",
            date=datetime(2024, 1, 9, 10, 30)
        )
        
        # Serialize to dict
        data = commit.model_dump()
        assert data["sha"] == "abc123"
        assert data["author"] == "dev-user"
        
        # Serialize to JSON
        json_str = commit.model_dump_json()
        assert "abc123" in json_str
        assert "dev-user" in json_str
    
    def test_feature_trace_defaults(self):
        """Test FeatureTrace default values"""
        trace = FeatureTrace(
            keyword="test",
            repo="org/repo"
        )
        
        # Verify defaults
        assert trace.file_matches == []
        assert trace.commit_matches == []
        assert trace.pr_matches == []
        assert trace.total_mentions == 0
        assert trace.first_mention_date is None
```

---

## Integration Testing Patterns

### Pattern 1: Basic Integration Test

```python
# tests/integration/test_feature_tracer_integration.py

import pytest
from gh_wrapper.features.feature_tracer import FeatureTracer


@pytest.mark.integration
class TestFeatureTracerIntegration:
    """Integration tests against real GitHub repositories"""
    
    def test_trace_public_repo(self):
        """Test tracing against cli/cli (known public repo)"""
        tracer = FeatureTracer()
        
        result = tracer.trace_feature(
            keyword="release",
            repos="cli/cli",
            branches=["trunk"],
            max_commits_per_branch=50
        )
        
        # Verify structure (not exact values, as they change)
        assert result.keyword == "release"
        assert "cli/cli" in result.repos_searched
        assert result.total_mentions_all_repos > 0
        
        trace = result.traces["cli/cli"]
        assert isinstance(trace.file_matches, list)
        assert isinstance(trace.commit_matches, list)
        assert isinstance(trace.pr_matches, list)
        
        # Should find at least some matches
        assert trace.total_mentions > 0
```

### Pattern 2: Using Test Fixtures

```python
# tests/conftest.py (shared fixtures)

import pytest
import os


@pytest.fixture
def skip_if_no_integration():
    """Skip test if integration tests not enabled"""
    if not os.getenv("RUN_INTEGRATION_TESTS"):
        pytest.skip("Integration tests not enabled (set RUN_INTEGRATION_TESTS=1)")


@pytest.fixture
def test_repo():
    """Known public repository for testing"""
    return "cli/cli"


# tests/integration/test_repo_analysis_integration.py

@pytest.mark.integration
def test_analyze_commit_patterns(skip_if_no_integration, test_repo):
    """Test commit analysis against real repo"""
    from gh_wrapper.features.repo_analysis import RepoAnalyzer
    from gh_wrapper.commands import CommitsManager
    
    commits_mgr = CommitsManager(test_repo)
    analyzer = RepoAnalyzer(commits_mgr)
    
    report = analyzer.analyze_commit_patterns(
        branches=["trunk"],
        days_back=30
    )
    
    # Verify report structure
    assert report.total_commits > 0
    assert len(report.top_contributors) > 0
    assert report.daily_trend is not None
```

### Pattern 3: Testing Against Test Branch

```python
# tests/integration/test_with_known_branch.py

import pytest
from gh_wrapper.commands import CommitsManager


@pytest.mark.integration
class TestWithKnownBranch:
    """Tests using our own test-branch-fixture"""
    
    def test_commits_on_test_branch(self):
        """Test against known test branch with predictable data"""
        # Using your actual test repo
        commits_mgr = CommitsManager("MohamedHamed19m/agent-gh-hub")
        
        commits = commits_mgr.get_commits(
            branch="test-branch-fixture",
            limit=10
        )
        
        assert len(commits) > 0
        assert all("sha" in c for c in commits)
        assert all("commit" in c for c in commits)
```

---

## Test Organization

### Directory Structure
```
tests/
├── conftest.py                  # Shared fixtures
├── __init__.py
│
├── unit/                        # Unit tests (mocked)
│   ├── commands/
│   │   ├── test_commits.py
│   │   ├── test_repository.py
│   │   └── test_pull_requests.py
│   │
│   ├── features/
│   │   ├── test_feature_tracer.py
│   │   ├── test_repo_analysis.py
│   │   └── test_branch_analytics.py
│   │
│   └── models/
│       ├── test_analysis.py
│       └── test_trace.py
│
└── integration/                 # Integration tests (real API)
    ├── test_feature_tracer_integration.py
    ├── test_repo_analysis_integration.py
    └── test_with_known_branch.py
```

### Naming Conventions
- Test files: `test_<module>.py`
- Test classes: `Test<ClassName>`
- Test methods: `test_<what_it_tests>`
- Integration tests: Add `@pytest.mark.integration` decorator

---

## Common Test Scenarios

### Testing Error Conditions

```python
def test_handles_empty_results(self, repo_manager, mock_executor):
    """Test handling of empty results from GitHub"""
    mock_executor.execute.return_value = "[]"
    
    result = repo_manager.list_branches()
    
    assert result == []
    assert isinstance(result, list)


def test_handles_invalid_json(self, repo_manager, mock_executor):
    """Test handling of malformed JSON response"""
    mock_executor.execute.return_value = "not valid json"
    
    with pytest.raises(json.JSONDecodeError):
        repo_manager.list_branches()


def test_handles_rate_limit_error(self, repo_manager, mock_executor):
    """Test handling of GitHub rate limit"""
    mock_executor.execute.side_effect = GHCommandError(
        "API rate limit exceeded",
        exit_code=1
    )
    
    with pytest.raises(GHCommandError) as exc:
        repo_manager.list_branches()
    
    assert "rate limit" in str(exc.value).lower()
```

### Testing Optional Parameters

```python
def test_default_parameters(self, feature, mock_managers):
    """Test method with default parameter values"""
    result = feature.analyze()  # No params
    
    # Verify defaults were used
    assert result is not None


def test_custom_parameters(self, feature, mock_managers):
    """Test method with custom parameters"""
    result = feature.analyze(
        branches=["main", "develop"],
        since="2024-01-01",
        limit=50
    )
    
    # Verify custom params were applied
    # Check via manager call verification
```

### Testing Date Handling

```python
def test_date_filtering(self, tracer):
    """Test date filtering in searches"""
    with patch.object(tracer, '_search_commits') as mock_search:
        tracer.trace_feature(
            "test",
            repos="org/repo",
            since_date="2024-01-01"
        )
        
        # Verify since_date was passed correctly
        call_args = mock_search.call_args
        assert call_args[1]["since_date"] == "2024-01-01"
```

---

## Continuous Integration

### Pre-commit Checks

```bash
# .pre-commit-config.yaml pattern
# Run before every commit

# Tests
uv run pytest tests/unit --cov=src/gh_wrapper

# Type checking
uv run mypy src/gh_wrapper

# Linting
uv run ruff check src/gh_wrapper tests/

# Formatting
uv run ruff format src/gh_wrapper tests/
```

### GitHub Actions

```yaml
# .github/workflows/test.yml (example pattern)
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Install uv
        run: curl -LsSf https://astral.sh/uv/install.sh | sh
      
      - name: Sync dependencies
        run: uv sync --all-extras
      
      - name: Run unit tests
        run: uv run pytest tests/unit --cov=src/gh_wrapper
      
      - name: Run type checking
        run: uv run mypy src/gh_wrapper
      
      - name: Run linting
        run: uv run ruff check src/gh_wrapper
```

---

## Coverage Best Practices

### What to Aim For
- **Overall:** >80% line coverage
- **Critical paths:** 100% coverage (core logic, error handling)
- **Edge cases:** Test happy path + error conditions

### What to Exclude
```python
# pyproject.toml
[tool.coverage.run]
omit = [
    "tests/*",
    "scripts/*",
    "*/conftest.py"
]
```

### Viewing Missing Coverage
```bash
# See which lines aren't covered
uv run pytest tests/unit --cov=src/gh_wrapper --cov-report=term-missing

# Example output:
# src/gh_wrapper/features/feature_tracer.py    87%   45-47, 102
#                                                     ^^^^^^^^
#                                                     Lines not covered
```

---

## TDD Workflow

### The Red-Green-Refactor Cycle

```
1. RED: Write failing test
   └─> uv run pytest tests/unit/features/test_feature.py -v
       FAILED

2. GREEN: Implement minimum code to pass
   └─> uv run pytest tests/unit/features/test_feature.py -v
       PASSED

3. REFACTOR: Improve code while keeping tests green
   └─> uv run pytest tests/unit/features/test_feature.py -v
       PASSED

4. REPEAT
```

### Example TDD Session

```bash
# 1. Write test first
# Edit: tests/unit/features/test_feature_tracer.py
# Add: def test_search_files()

# 2. Run test (should fail)
uv run pytest tests/unit/features/test_feature_tracer.py::TestFeatureTracer::test_search_files -v
# FAILED (method doesn't exist)

# 3. Implement method
# Edit: src/gh_wrapper/features/feature_tracer.py
# Add: def _search_files(...)

# 4. Run test (should pass)
uv run pytest tests/unit/features/test_feature_tracer.py::TestFeatureTracer::test_search_files -v
# PASSED

# 5. Refactor and verify
# Edit: Improve implementation
uv run pytest tests/unit/features/test_feature_tracer.py -v
# All PASSED

# 6. Check coverage
uv run pytest tests/unit/features/test_feature_tracer.py --cov=src/gh_wrapper/features/feature_tracer
# 85% coverage ✓
```

---

## Quick Reference

### Essential Commands
```bash
# Unit tests only
uv run pytest tests/unit

# With coverage
uv run pytest tests/unit --cov=src/gh_wrapper --cov-report=term-missing

# Integration tests
export RUN_INTEGRATION_TESTS=1
uv run pytest tests/integration

# Specific test
uv run pytest tests/unit/features/test_feature_tracer.py::TestFeatureTracer::test_method -v

# Show print statements
uv run pytest tests/unit -v -s

# Stop on first failure
uv run pytest tests/unit -x
```

### Useful Pytest Options
- `-v`: Verbose output
- `-s`: Show print statements
- `-x`: Stop on first failure
- `-k "pattern"`: Run tests matching pattern
- `--lf`: Run last failed tests
- `--pdb`: Drop into debugger on failure

---

## Troubleshooting

### Common Issues

**Issue: Mock not being called**
```python
# Problem: Mock class instead of instance
mock_file_mgr.search_in_files.assert_called()  # Fails

# Solution: Patch the class, mock the instance
@patch("module.FileManager")
def test(mock_class):
    mock_instance = Mock()
    mock_class.return_value = mock_instance
    # Now mock_instance.search_in_files.assert_called() works
```

**Issue: Coverage not updating**
```bash
# Clear pytest cache
rm -rf .pytest_cache/
rm -rf .coverage

# Re-run tests
uv run pytest tests/unit --cov=src/gh_wrapper
```

**Issue: Integration tests timing out**
```python
# Add timeout marker
@pytest.mark.timeout(30)
@pytest.mark.integration
def test_slow_operation():
    ...
```

---

## Resources

- **Pytest Docs:** https://docs.pytest.org/
- **Coverage.py:** https://coverage.readthedocs.io/
- **Mocking Guide:** https://docs.python.org/3/library/unittest.mock.html
- **TDD Guide:** Kent Beck's "Test Driven Development"

---

For specific patterns in this codebase, refer to:
- [Adding Commands Guide](./adding-commands.md)
- [Adding Features Guide](./adding-features.md)