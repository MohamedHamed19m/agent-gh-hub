# 🌉 gh-bridge

A robust, Pythonic wrapper around the **GitHub CLI (`gh`)**, engineered specifically for **AI Agents** (like Claude, Gemini, and GPT) and high-automation environments.

[![Tests](https://github.com/MohamedHamed19m/agent-gh-hub/actions/workflows/test.yml/badge.svg)](https://github.com/MohamedHamed19m/agent-gh-hub/actions/workflows/test.yml)
[![Python Version](https://img.shields.io/badge/python-3.10%2B-blue)](https://python.org)
[![Managed by uv](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/uv/main/assets/badge/v0.json)](https://github.com/astral-sh/uv)

![gh-bridge Architecture](docs/package_image.png)

## 🎯 Why gh-bridge?

In many **Enterprise environments**, security policies often restrict Personal Access Tokens. `gh-bridge` solves this by acting as a **Pythonic wrapper for the GitHub CLI (`gh`)**, leveraging your existing authenticated CLI session to navigate SAML/SSO requirements seamlessly.

- **SAML/SSO Compatibility:** Inherits your browser-based SSO session.
- **Zero Credential Management:** Uses the local system's secure credential store.
- **AI-Native Output:** Parses CLI output into structured JSON/TOON for LLM context windows.

## 🛠️ Key Features

- **📊 Branch Analytics:** Analyze activity and health metrics.
- **🔍 Feature Tracer:** Search logic across multiple repositories.
- **🤖 PR Review:** Automated review suggestions and summaries.
- **👤 User Activity:** Trace a developer's recent progress and intent.
- **📂 Repo Contextualizer:** "Big Picture" view for AI agents.

## 🚀 Quick Start

### Prerequisites
1. [GitHub CLI](https://cli.github.com/) installed and authenticated (`gh auth login`).
2. [uv](https://github.com/astral-sh/uv) installed.

### Installation
```bash
git clone https://github.com/MohamedHamed19m/gh-bridge
cd gh-bridge
uv sync --all-extras
```

## 📖 Documentation

Detailed usage guides are available for both CLI and Library users:

- **[💻 CLI Usage Guide](docs/cli_usage_example.md):** How to use the `gh-bridge` command-line interface.
- **[🐍 Python API Guide](docs/lib_usage_example.md):** How to integrate `gh-bridge` into your Python projects.
- **[🎨 Visual Demos](docs/lib_usage_example.md#visual-demos):** Run interactive demo scripts from the `scripts/` directory.

## 🏗️ Project Structure

```
src/gh_wrapper/
├── cli/            # CLI implementation (Typer)
├── core/           # Core framework (Executor, Cache)
├── commands/       # Low-level API Wrappers
├── features/       # High-level logic (Tracer, Analytics)
└── models/         # Pydantic data models
```

## 🧪 Testing

```bash
# Run all tests (requires authenticated gh CLI)
$env:RUN_INTEGRATION_TESTS='1'; uv run pytest
```

## 🤝 Contributing
Contributions are welcome! Please ensure all PRs pass the ruff linting and mypy type checks.

Created by MohamedHamed19m