# 🌉 gh-bridge

**gh-bridge** is a high-performance Python library and CLI tool that acts as a robust wrapper around the **GitHub CLI (`gh`)**. Engineered specifically for **AI Agents** (like Claude, Gemini, and GPT) and high-automation environments, it provides a seamless way to access GitHub data in enterprise settings where direct Personal Access Token usage is restricted by **SAML/SSO** policies.

By leveraging your local authenticated GitHub CLI session, `gh-bridge` enables automated code analysis, repository tracing, and PR management without complex credential handling. It transforms raw CLI output into **AI-native structured data (JSON/TOON)**, perfectly optimized for LLM context windows.

---

[![Tests](https://github.com/MohamedHamed19m/agent-gh-hub/actions/workflows/test.yml/badge.svg)](https://github.com/MohamedHamed19m/agent-gh-hub/actions/workflows/test.yml)
[![Python Version](https://img.shields.io/badge/python-3.10%2B-blue)](https://python.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Managed by uv](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/uv/main/assets/badge/v0.json)](https://github.com/astral-sh/uv)

![Architecture diagram of gh-bridge AI Agent workflow showing Python-to-GitHub CLI integration](docs/package_image.png)

---

## 📋 Table of Contents

- [🎯 Why gh-bridge?](#-why-gh-bridge)
- [🛠️ Key Features](#️-key-features)
- [🚀 Quick Start](#-quick-start)
- [📖 Documentation](#-documentation)
- [🏗️ Project Structure](#️-project-structure)
- [🧪 Testing](#-testing)
- [🤝 Contributing](#-contributing)

---

## 🎯 Why gh-bridge?

In many **Enterprise environments**, security policies restrict Personal Access Tokens. `gh-bridge` solves this by acting as a **Pythonic bridge**, inheriting your browser-based SSO session seamlessly.

- **SAML/SSO Compatibility:** Works anywhere the `gh` CLI is authenticated.
- **Zero Credential Management:** Uses the local system's secure credential store.
- **AI-Native Output:** Parses CLI output into structured Pydantic models for automated agents.

## 🛠️ Key Features

- **📊 Branch Analytics:** Detailed activity, health metrics, and contributor stats.
- **🔍 Feature Tracer:** Multi-repo search for logic, keywords, or code snippets.
- **🤖 PR Review:** Automated review suggestions and impact summaries.
- **👤 User Activity:** Trace developer progress and intent across branches.
- **📂 Repo Contextualizer:** Unified "Big Picture" view for LLM context gathering.

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

Explore detailed guides for your specific use case:

- **[💻 CLI Usage Guide](docs/cli_usage_example.md):** Master the `gh-bridge` command-line tool.
- **[🐍 Python API Guide](docs/lib_usage_example.md):** Deep integration into your Python automation.
- **[🎨 Visual Demos](docs/lib_usage_example.md#visual-demos):** Run interactive scripts from the `scripts/` directory.

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

Created by **MohamedHamed19m**
