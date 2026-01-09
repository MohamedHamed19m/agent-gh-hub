# Adding Feature Layer Orchestration

## Overview

The **Feature Layer** composes Command Layer wrappers to provide high-level insights, aggregations, and AI-optimized outputs. Features orchestrate multiple commands, perform calculations, and return structured Pydantic models.

### The Golden Rule
> **Features Compose Commands, Commands Fetch Data**
> 
> If you're wrapping a single `gh` CLI call, you're building a **Command**, not a Feature.

### When to Add a Feature
- ✅ You need to combine data from multiple commands
- ✅ You want to calculate metrics, trends, or rankings
- ✅ You need to provide AI-optimized summaries
- ✅ You're aggregating results across branches/repos

### When NOT to Add a Feature
- ❌ You just need raw GitHub data → **Use Commands directly**
- ❌ Single `gh` CLI call with no logic → **Add a Command**

---

## Prerequisites Checklist

Before building a feature, verify:

- [ ] **Command Layer Audit**: Do existing commands provide the data you need?
  ```python
  # Check what's available:
  from gh_wrapper.commands import (
      RepoManager,      # Repo metadata, branches, file structure
      CommitsManager,   # Commit history and details
      PRManager,        # Pull requests
      FileManager,      # File content and search
      UsersManager      # User information
  )
  ```

- [ ] **Design Pydantic Models**: Plan your output structure
  - Create models in `src/gh_wrapper/models/<domain>.py`
  - Use descriptive field names and types
  - Add helpful docstrings

- [ ] **Plan Feature API**: Design clean, intuitive methods
  - Keep parameters simple
  - Return Pydantic models (not dicts)
  - Provide optional formatting methods

- [ ] **Consider Performance**:
  - Will you process large datasets?
  - Do you need caching?
  - Should operations run in parallel?

---

## Architecture Decision Tree

```
Need GitHub data?
├─ Single gh CLI call? → Add COMMAND
├─ Multiple data sources? → Continue below
│
Need to combine/aggregate?
├─ Simple filtering? → Do in client code
├─ Complex logic? → Add FEATURE
│
Feature will:
├─ Compose multiple commands → ✅ Correct layer
├─ Calculate metrics → ✅ Correct layer
├─ Return Pydantic models → ✅ Correct layer
└─ Provide AI-optimized output → ✅ Correct layer
```

---

## Step-by-Step Implementation Guide

### Phase 1: Models & Foundation

#### 1.1 Design Pydantic Models

**Example: Feature Tracer**
```python
# src/gh_wrapper/models/trace.py

from pydantic import BaseModel, Field
from typing import List, Dict, Optional
from datetime import datetime


class FileMatch(BaseModel):
    """Single file search result"""
    path: str = Field(..., description="File path relative to repo root")
    line_count: int = Field(..., description="Number of matching lines")
    snippets: List[str] = Field(default_factory=list, description="Code snippets (max 3)")


class TraceCommit(BaseModel):
    """Commit matching the search keyword"""
    sha: str = Field(..., description="Commit SHA")
    message: str = Field(..., description="Commit message")
    author: str = Field(..., description="Author username")
    date: datetime = Field(..., description="Commit timestamp")


class TracePR(BaseModel):
    """Pull request matching the search keyword"""
    number: int = Field(..., description="PR number")
    title: str = Field(..., description="PR title")
    author: str = Field(..., description="Author username")
    state: str = Field(..., description="PR state (open/closed/merged)")
    created_at: datetime = Field(..., description="Creation timestamp")


class FeatureTrace(BaseModel):
    """Feature trace results for a single repository"""
    keyword: str = Field(..., description="Search keyword")
    repo: str = Field(..., description="Repository (owner/repo)")
    
    # Search results
    file_matches: List[FileMatch] = Field(default_factory=list)
    commit_matches: List[TraceCommit] = Field(default_factory=list)
    pr_matches: List[TracePR] = Field(default_factory=list)
    contributors: List[Dict[str, int]] = Field(
        default_factory=list,
        description="Contributor stats: {username, commit_count, pr_count}"
    )
    
    # Metadata
    total_mentions: int = Field(0, description="Total matches across all sources")
    first_mention_date: Optional[datetime] = Field(None)
    last_activity_date: Optional[datetime] = Field(None)


class MultiRepoFeatureTrace(BaseModel):
    """Aggregated results from multiple repositories"""
    keyword: str
    repos_searched: List[str]
    traces: Dict[str, FeatureTrace] = Field(
        ...,
        description="Per-repo traces keyed by repository name"
    )
    
    # Aggregated stats
    total_mentions_all_repos: int = Field(0)
    repos_with_matches: int = Field(0)
    top_contributors_global: List[Dict] = Field(default_factory=list)
    
    def get_trace(self, repo: str) -> Optional[FeatureTrace]:
        """Get trace for specific repository"""
        return self.traces.get(repo)
```

#### 1.2 Write Model Tests
```python
# tests/unit/models/test_trace.py

import pytest
from datetime import datetime
from gh_wrapper.models.trace import FileMatch, TraceCommit, FeatureTrace


class TestTraceModels:
    """Test Pydantic models for feature tracing"""
    
    def test_file_match_creation(self):
        """Test FileMatch model validation"""
        match = FileMatch(
            path="src/main.py",
            line_count=3,
            snippets=["def secure_boot():", "# Secure boot logic", "return True"]
        )
        
        assert match.path == "src/main.py"
        assert match.line_count == 3
        assert len(match.snippets) == 3
    
    def test_trace_commit_validation(self):
        """Test TraceCommit model validation"""
        commit = TraceCommit(
            sha="abc123",
            message="Add secure boot feature",
            author="dev-user",
            date=datetime.now()
        )
        
        assert commit.sha == "abc123"
        assert "secure boot" in commit.message
    
    def test_feature_trace_aggregation(self):
        """Test FeatureTrace calculates total mentions"""
        trace = FeatureTrace(
            keyword="secure boot",
            repo="org/backend",
            file_matches=[FileMatch(path="a.py", line_count=2, snippets=[])],
            commit_matches=[TraceCommit(
                sha="abc",
                message="msg",
                author="user",
                date=datetime.now()
            )],
            pr_matches=[],
            total_mentions=3  # 2 files + 1 commit
        )
        
        assert trace.total_mentions == 3
        assert len(trace.file_matches) == 1
        assert len(trace.commit_matches) == 1
    
    def test_feature_trace_serialization(self):
        """Test model can serialize to JSON"""
        trace = FeatureTrace(
            keyword="test",
            repo="org/repo",
            total_mentions=0
        )
        
        json_data = trace.model_dump_json()
        assert "keyword" in json_data
        assert "test" in json_data
```

#### 1.3 Export Models
```python
# src/gh_wrapper/models/__init__.py

from .analysis import BranchStats, CommitAnalysisReport
from .trace import (
    FileMatch,
    TraceCommit,
    TracePR,
    FeatureTrace,
    MultiRepoFeatureTrace
)

__all__ = [
    "BranchStats",
    "CommitAnalysisReport",
    "FileMatch",
    "TraceCommit",
    "TracePR",
    "FeatureTrace",
    "MultiRepoFeatureTrace",
]
```

---

### Phase 2: Core Logic (TDD Approach)

#### 2.1 Scaffold Feature Class
```python
# src/gh_wrapper/features/feature_tracer.py

"""Feature tracing across repositories, commits, PRs, and contributors."""

from typing import List, Dict, Union, Optional
from collections import defaultdict
from datetime import datetime

from ..models.trace import (
    FileMatch,
    TraceCommit,
    TracePR,
    FeatureTrace,
    MultiRepoFeatureTrace
)
from ..commands import FileManager, CommitsManager, PRManager


class FeatureTracer:
    """
    Search for features across repositories.
    
    Provides comprehensive cross-sectional analysis by searching:
    - Code files for keyword mentions
    - Commit messages
    - Pull request titles and descriptions
    - Contributors working on the feature
    
    Example:
        >>> tracer = FeatureTracer()
        >>> result = tracer.trace_feature(
        ...     keyword="secure boot",
        ...     repos=["org/backend", "org/firmware"]
        ... )
        >>> print(f"Found in {result.repos_with_matches} repositories")
    """
    
    def __init__(self):
        """Initialize stateless tracer (repos passed per search)"""
        pass
    
    def trace_feature(
        self,
        keyword: str,
        repos: Union[str, List[str]],
        branches: Optional[List[str]] = None,
        since_date: Optional[str] = None,
        search_files: bool = True,
        search_commits: bool = True,
        search_prs: bool = True,
        max_commits_per_branch: int = 100
    ) -> MultiRepoFeatureTrace:
        """
        Execute comprehensive feature search.
        
        Args:
            keyword: Search term (e.g., "secure boot", "authentication")
            repos: Single repository or list of repositories
            branches: Branches to search (default: ["main"])
            since_date: Filter activity after this date (YYYY-MM-DD)
            search_files: Enable file/code search
            search_commits: Enable commit message search
            search_prs: Enable PR title/body search
            max_commits_per_branch: Limit commits fetched per branch
        
        Returns:
            MultiRepoFeatureTrace with per-repo traces and aggregated stats
        """
        # Normalize repos to list
        repo_list = [repos] if isinstance(repos, str) else repos
        branches = branches or ["main"]
        
        # Search each repository
        traces = {}
        for repo in repo_list:
            trace = self._trace_single_repo(
                repo=repo,
                keyword=keyword,
                branches=branches,
                since_date=since_date,
                search_files=search_files,
                search_commits=search_commits,
                search_prs=search_prs,
                max_commits_per_branch=max_commits_per_branch
            )
            traces[repo] = trace
        
        # Calculate aggregated statistics
        total_mentions = sum(t.total_mentions for t in traces.values())
        repos_with_matches = sum(1 for t in traces.values() if t.total_mentions > 0)
        top_contributors = self._aggregate_contributors(traces.values())
        
        return MultiRepoFeatureTrace(
            keyword=keyword,
            repos_searched=repo_list,
            traces=traces,
            total_mentions_all_repos=total_mentions,
            repos_with_matches=repos_with_matches,
            top_contributors_global=top_contributors
        )
    
    def _trace_single_repo(
        self,
        repo: str,
        keyword: str,
        branches: List[str],
        since_date: Optional[str],
        search_files: bool,
        search_commits: bool,
        search_prs: bool,
        max_commits_per_branch: int
    ) -> FeatureTrace:
        """Trace feature in a single repository (to be implemented)"""
        # Create managers for this repo
        file_mgr = FileManager(repo)
        commits_mgr = CommitsManager(repo)
        pr_mgr = PRManager(repo)
        
        # Execute searches
        file_matches = self._search_files(file_mgr, keyword) if search_files else []
        commit_matches = self._search_commits(
            commits_mgr, keyword, branches, since_date, max_commits_per_branch
        ) if search_commits else []
        pr_matches = self._search_prs(pr_mgr, keyword) if search_prs else []
        
        # Analyze contributors
        contributors = self._analyze_contributors(commit_matches, pr_matches)
        
        # Calculate metadata
        total_mentions = len(file_matches) + len(commit_matches) + len(pr_matches)
        dates = [c.date for c in commit_matches] + [p.created_at for p in pr_matches]
        
        return FeatureTrace(
            keyword=keyword,
            repo=repo,
            file_matches=file_matches,
            commit_matches=commit_matches,
            pr_matches=pr_matches,
            contributors=contributors,
            total_mentions=total_mentions,
            first_mention_date=min(dates) if dates else None,
            last_activity_date=max(dates) if dates else None
        )
    
    def _search_files(self, file_mgr: FileManager, keyword: str) -> List[FileMatch]:
        """Search files for keyword (to be implemented)"""
        pass
    
    def _search_commits(
        self,
        commits_mgr: CommitsManager,
        keyword: str,
        branches: List[str],
        since_date: Optional[str],
        limit: int
    ) -> List[TraceCommit]:
        """Search commits by message content (to be implemented)"""
        pass
    
    def _search_prs(self, pr_mgr: PRManager, keyword: str) -> List[TracePR]:
        """Search PRs by title/body (to be implemented)"""
        pass
    
    def _analyze_contributors(
        self,
        commits: List[TraceCommit],
        prs: List[TracePR]
    ) -> List[Dict[str, int]]:
        """Aggregate contributor statistics (to be implemented)"""
        pass
    
    def _aggregate_contributors(
        self,
        traces: List[FeatureTrace]
    ) -> List[Dict]:
        """Aggregate top contributors across all repos (to be implemented)"""
        pass
```

#### 2.2 Write Feature Tests (TDD)
```python
# tests/unit/features/test_feature_tracer.py

import pytest
from unittest.mock import Mock, patch
from datetime import datetime

from gh_wrapper.features.feature_tracer import FeatureTracer
from gh_wrapper.models.trace import (
    FileMatch,
    TraceCommit,
    TracePR,
    FeatureTrace
)


class TestFeatureTracer:
    """Test FeatureTracer functionality"""
    
    @pytest.fixture
    def tracer(self):
        """FeatureTracer instance"""
        return FeatureTracer()
    
    @patch("gh_wrapper.features.feature_tracer.FileManager")
    @patch("gh_wrapper.features.feature_tracer.CommitsManager")
    @patch("gh_wrapper.features.feature_tracer.PRManager")
    def test_trace_single_repo(
        self,
        mock_pr_mgr_class,
        mock_commits_mgr_class,
        mock_file_mgr_class,
        tracer
    ):
        """Test tracing a single repository"""
        # Mock the managers
        mock_file_mgr = Mock()
        mock_commits_mgr = Mock()
        mock_pr_mgr = Mock()
        
        mock_file_mgr_class.return_value = mock_file_mgr
        mock_commits_mgr_class.return_value = mock_commits_mgr
        mock_pr_mgr_class.return_value = mock_pr_mgr
        
        # Mock search results
        mock_file_mgr.search_in_files.return_value = [
            {"path": "src/boot.py", "lines": ["def secure_boot():"]}
        ]
        mock_commits_mgr.get_commits.return_value = [
            {
                "sha": "abc123",
                "commit": {
                    "message": "Add secure boot feature",
                    "author": {"name": "dev", "date": "2024-01-01T10:00:00Z"}
                }
            }
        ]
        mock_pr_mgr.list_prs.return_value = []
        
        # Execute trace
        result = tracer.trace_feature(
            keyword="secure boot",
            repos="org/backend"
        )
        
        # Verify results
        assert isinstance(result, MultiRepoFeatureTrace)
        assert result.keyword == "secure boot"
        assert "org/backend" in result.repos_searched
        assert result.repos_with_matches == 1
    
    def test_normalize_repos_input(self, tracer):
        """Test repos parameter normalization"""
        # Single string
        with patch.object(tracer, '_trace_single_repo') as mock_trace:
            mock_trace.return_value = FeatureTrace(
                keyword="test",
                repo="org/repo",
                total_mentions=0
            )
            
            result = tracer.trace_feature("test", repos="org/repo")
            assert len(result.repos_searched) == 1
            
        # List of strings
        with patch.object(tracer, '_trace_single_repo') as mock_trace:
            mock_trace.return_value = FeatureTrace(
                keyword="test",
                repo="org/repo",
                total_mentions=0
            )
            
            result = tracer.trace_feature("test", repos=["org/repo1", "org/repo2"])
            assert len(result.repos_searched) == 2
```

#### 2.3 Implement Core Logic
Implement each private helper method one at a time, writing tests first:

1. `_search_files()` → Use `FileManager.search_in_files()`
2. `_search_commits()` → Use `CommitsManager.get_commits()` + filter
3. `_search_prs()` → Use `PRManager.list_prs()` + filter
4. `_analyze_contributors()` → Aggregate from commits/PRs
5. `_aggregate_contributors()` → Global top contributors

---

### Phase 3: Integration & Demo

#### 3.1 Write Integration Test
```python
# tests/integration/test_feature_tracer_integration.py

import pytest
from gh_wrapper.features.feature_tracer import FeatureTracer


@pytest.mark.integration
class TestFeatureTracerIntegration:
    """Integration tests against real repositories"""
    
    def test_trace_public_repo(self):
        """Test tracing against cli/cli repository"""
        tracer = FeatureTracer()
        
        result = tracer.trace_feature(
            keyword="release",
            repos="cli/cli",
            branches=["trunk"],
            max_commits_per_branch=50
        )
        
        assert result.keyword == "release"
        assert "cli/cli" in result.repos_searched
        assert result.total_mentions_all_repos > 0
        
        # Verify trace structure
        trace = result.traces["cli/cli"]
        assert isinstance(trace.file_matches, list)
        assert isinstance(trace.commit_matches, list)
        assert isinstance(trace.pr_matches, list)
```

#### 3.2 Create Demo Script
```python
# scripts/demo_feature_tracer.py

"""
Demo: Feature Tracer

Search for a keyword across repositories to understand feature development.
"""

from rich.console import Console
from rich.table import Table
from gh_wrapper.features.feature_tracer import FeatureTracer


def main():
    console = Console()
    
    console.print("\n[bold cyan]Feature Tracer Demo[/bold cyan]")
    console.print("Searching for 'release' in cli/cli repository...\n")
    
    # Initialize tracer
    tracer = FeatureTracer()
    
    # Execute search
    result = tracer.trace_feature(
        keyword="release",
        repos="cli/cli",
        branches=["trunk"],
        max_commits_per_branch=50
    )
    
    # Display results
    trace = result.traces["cli/cli"]
    
    console.print(f"[green]✓[/green] Found {trace.total_mentions} mentions\n")
    
    # Files table
    if trace.file_matches:
        files_table = Table(title="File Matches")
        files_table.add_column("Path", style="cyan")
        files_table.add_column("Lines", justify="right")
        
        for match in trace.file_matches[:5]:
            files_table.add_row(match.path, str(match.line_count))
        
        console.print(files_table)
    
    # Contributors table
    if trace.contributors:
        contrib_table = Table(title="Top Contributors")
        contrib_table.add_column("Username", style="yellow")
        contrib_table.add_column("Commits", justify="right")
        contrib_table.add_column("PRs", justify="right")
        
        for contrib in trace.contributors[:10]:
            contrib_table.add_row(
                contrib["username"],
                str(contrib["commit_count"]),
                str(contrib["pr_count"])
            )
        
        console.print(contrib_table)


if __name__ == "__main__":
    main()
```

Run demo:
```bash
uv run scripts/demo_feature_tracer.py
```

---

### Phase 4: Documentation

#### 4.1 Update README.md
```markdown
### Feature Tracer

Search for features across repositories, commits, PRs, and contributors:

```python
from gh_wrapper.features import FeatureTracer

tracer = FeatureTracer()
result = tracer.trace_feature(
    keyword="secure boot",
    repos=["org/backend", "org/firmware"],
    branches=["main", "develop"],
    since_date="2024-01-01"
)

# Access results
for repo, trace in result.traces.items():
    print(f"{repo}: {trace.total_mentions} mentions")
    print(f"  Contributors: {len(trace.contributors)}")
```
```

#### 4.2 Update docs/Usage_example.md
Add comprehensive examples with expected output.

#### 4.3 Update GEMINI.md (AI Context)
```markdown
## Feature: Feature Tracer

**Purpose:** Cross-sectional feature analysis across repositories

**Models:** `FeatureTrace`, `MultiRepoFeatureTrace` (in `models/trace.py`)

**Methods:**
- `trace_feature(keyword, repos, ...)` → Search across dimensions
- Composes: `FileManager`, `CommitsManager`, `PRManager`
- Returns: Pydantic models with aggregated insights

**Testing:**
- Unit: Mock all managers, test aggregation logic
- Integration: Test against public repos (cli/cli)
```

---

## Common Patterns

### Pattern 1: Client-Side Filtering
```python
def _search_commits(self, commits_mgr, keyword, ...):
    """Fetch all commits, filter client-side"""
    all_commits = commits_mgr.get_commits(branch=branch, limit=limit)
    
    # Filter by message content
    matches = [
        c for c in all_commits
        if keyword.lower() in c['commit']['message'].lower()
    ]
    
    return [self._parse_commit(c) for c in matches]
```

### Pattern 2: Contributor Aggregation
```python
def _analyze_contributors(self, commits, prs):
    """Aggregate contributor stats"""
    from collections import defaultdict
    
    stats = defaultdict(lambda: {"commit_count": 0, "pr_count": 0})
    
    for commit in commits:
        stats[commit.author]["commit_count"] += 1
    
    for pr in prs:
        stats[pr.author]["pr_count"] += 1
    
    # Return sorted by total activity
    return sorted(
        [{"username": k, **v} for k, v in stats.items()],
        key=lambda x: x["commit_count"] + x["pr_count"],
        reverse=True
    )
```

### Pattern 3: Optional Formatting
```python
def format_trace_summary(self, trace: FeatureTrace) -> str:
    """Generate Markdown summary"""
    return f"""
# Feature Trace: "{trace.keyword}"
Repository: {trace.repo}

## Summary
- Total Mentions: {trace.total_mentions}
- Files: {len(trace.file_matches)}
- Commits: {len(trace.commit_matches)}
- PRs: {len(trace.pr_matches)}

## Top Contributors
{self._format_contributors(trace.contributors[:10])}
"""
```

---

## Checklist for Feature Completion

- [ ] Pydantic models created and tested
- [ ] Feature class scaffolded
- [ ] Core logic implemented (TDD)
- [ ] Unit tests achieve >80% coverage
- [ ] Integration test passes
- [ ] Demo script created and tested
- [ ] README.md updated
- [ ] docs/Usage_example.md updated
- [ ] GEMINI.md updated
- [ ] Mypy passes
- [ ] Ruff linter passes
- [ ] Exported in `features/__init__.py`

---

## Next Steps

- Review [Testing Guide](./testing-guide.md) for detailed test patterns
- Check [Adding Commands](./adding-commands.md) if you need new data sources
- Create GitHub issue for tracking if it's a major feature

---

## Reference

- **Feature Examples:** `src/gh_wrapper/features/`
- **Model Examples:** `src/gh_wrapper/models/`
- **Demo Examples:** `scripts/demo_*.py`
- **Test Examples:** `tests/unit/features/`