# 🌉 gh-bridge

A robust, Pythonic wrapper around the **GitHub CLI (`gh`)**, engineered specifically for **AI Agents** (like Claude, Gemini, and GPT) and high-automation environments.

[![CI/CD](https://github.com/MohamedHamed19m/gh-bridge/actions/workflows/test.yml/badge.svg)](https://github.com/MohamedHamed19m/gh-bridge/actions)
[![Python Version](https://img.shields.io/badge/python-3.10%2B-blue)](https://python.org)
[![Managed by uv](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/uv/main/assets/badge/v0.json)](https://github.com/astral-sh/uv)

## 🎯 Why gh-bridge?

While libraries like `PyGithub` or `ghapi` exist, `gh-bridge` leverages the **GitHub CLI** to handle complex Enterprise SSO, local credential caching, and advanced search features that are cumbersome via raw REST APIs. It outputs **AI-optimized JSON**, making it the perfect "eyes and ears" for your coding agents.

## 🛠️ Key Features

* **📊 Branch Analytics:** Analyze commit activity, contributors, and branch health metrics (`gh_wrapper.features.branch_analytics`).
* **🔍 Feature Tracer:** Search for logic or snippets across multiple repositories and branches (`gh_wrapper.features.feature_tracer`).
* **👤 User Activity Analytics:** Trace a developer's recent work to understand intent and progress (`gh_wrapper.features.user_tracer`).
* **📂 Repo Contextualizer:** One-call "Big Picture" view (Files, PRs, Branches, and README) for LLM context windows (`gh_wrapper.features.repo_context`).
* **📝 Core Commands:** specialized wrappers for Commits, Pull Requests, Files, and Repository management.
* **⚡ Built with `uv`:** Lightning-fast dependency management and environment setup.

## 🚀 Quick Start

### Prerequisites
1. [GitHub CLI](https://cli.github.com/) installed and authenticated (`gh auth login`).
2. [uv](https://github.com/astral-sh/uv) installed.

### Setup
```bash
# Clone the repo
git clone https://github.com/MohamedHamed19m/gh-bridge
cd gh-bridge

# Sync environment
uv sync --all-extras
```

### Usage

**Basic Repository Context:**
```python
from gh_wrapper.core.executor import GHExecutor
from gh_wrapper.features.repo_context import RepoContextGatherer

# Initialize executor with target repository
executor = GHExecutor(repo="owner/repo")

# Gather high-level context
gatherer = RepoContextGatherer(executor)
context = gatherer.get_context()

print(f"Repository: {context.summary['name']}")
print(f"Files found: {len(context.structure)}")
```

**Tracing Code Features:**
```python
from gh_wrapper.features.feature_tracer import FeatureTracer

tracer = FeatureTracer(executor)
# Search for 'auth' logic across main and develop branches
results = tracer.trace_code("auth", branches=["main", "develop"])
```

**Branch Activity Analytics:**
```python
from gh_wrapper.features.branch_analytics import BranchAnalyzer

analyzer = BranchAnalyzer(executor)
stats = analyzer.analyze_branch("main")

print(f"Branch: {stats.branch}")
print(f"Total Commits: {stats.total_commits}")
print(f"Top Contributor: {max(stats.contributors, key=stats.contributors.get)}")
```

**Running the Demo:**
```bash
python scripts/demo_usage.py
```

## 🏗️ Project Structure

```
src/gh_wrapper/
├── core/           # Core framework (Executor, Cache, Exceptions)
├── commands/       # API Wrappers (Commits, PRs, Files, Users)
└── features/       # High-level logic (Feature Tracer, Repo Context)
```

## 🧪 Testing

```bash
# Run unit tests
uv run pytest tests/unit

# Run integration tests (requires GH_TOKEN)
export RUN_INTEGRATION_TESTS=1
uv run pytest tests/integration
```

## 🤝 Contributing
Contributions are welcome! Please ensure all PRs pass the ruff linting and mypy type checks.

Created by MohamedHamed19m
