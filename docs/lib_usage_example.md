# Python API Usage Guide

This guide provides detailed examples of how to use the `gh-bridge` library directly in your Python code.

## 🏗️ Core Executor

All features require a `GHExecutor` instance. This handles the communication with the GitHub CLI and optional caching.

```python
from gh_wrapper.core.executor import GHExecutor

# Initialize for a specific repository
executor = GHExecutor(repo="owner/repo", use_cache=True)
```

## 📂 Repository Contextualizer

One-call "Big Picture" view of a repository, optimized for AI agent context windows.

```python
from gh_wrapper.features.repo_context import RepoContextAnalyzer

analyzer = RepoContextAnalyzer(executor)
report = analyzer.analyze_current_context(branch="main")

print(f"Repository: {report.target}")
print(f"Default Branch: {report.metadata.default_branch}")
print(f"Files found: {len(report.structure)}")
print(f"Recent Commits: {len(report.activity.recent_commits)}")
```

## 🔍 Feature Tracer

Search for logic or snippets across multiple repositories and branches.

```python
from gh_wrapper.features.feature_tracer import FeatureTracer

tracer = FeatureTracer()
# Search for 'authentication' logic across multiple repos
report = tracer.trace_feature("authentication", repos=["owner/repo1", "owner/repo2"])

for repo, trace in report.traces.items():
    print(f"Repo: {repo}, Mentions: {trace.total_mentions}")
```

## 📊 Branch Analytics

Analyze commit activity, contributors, and branch health metrics.

```python
from gh_wrapper.features.branch_analytics import BranchAnalyzer

analyzer = BranchAnalyzer(executor)
stats = analyzer.analyze_branch("main")

print(f"Branch: {stats.branch}")
print(f"Health Score: {stats.health_score}/100")
print(f"Total Commits (sampled): {stats.total_commits}")
```

## 👤 User Activity Analytics

Trace a developer's recent work to understand intent and progress.

```python
from gh_wrapper.features.user_tracer import UserTracer

tracer = UserTracer(executor)
# Trace recent work for a user
recent_work = tracer.trace_recent_work("username", "owner/repo")

for commit in recent_work:
    print(f"- {commit.sha[:7]}: {commit.message} ({commit.branch})")
```

## 🤖 PR Review

Automated change summary and review suggestions for Pull Requests.

```python
from gh_wrapper.features.pr_review_analyzer import PrReviewAnalyzer
from gh_wrapper.commands.pull_requests import PRManager
from gh_wrapper.models.pr_review import PrReviewInput

pr_manager = PRManager(executor)
analyzer = PrReviewAnalyzer(pr_manager)

pr_input = PrReviewInput(repo_name="owner/repo", pr_id=123)
report = analyzer.analyze_pr(pr_input)

# Get human-readable markdown
markdown = analyzer.format_as_markdown(report)
print(markdown)
```

## 📝 Core Command Wrappers

For direct access to GitHub data without high-level feature logic.

```python
from gh_wrapper.commands.files import FileManager
from gh_wrapper.commands.commits import CommitsManager

# Read file content
file_manager = FileManager(executor)
content = file_manager.get_file_content("pyproject.toml")

# List commits
commits_manager = CommitsManager(executor)
commits = commits_manager.list_commits(limit=5)
```
