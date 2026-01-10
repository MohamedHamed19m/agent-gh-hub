# CLI Usage Guide

`gh-bridge` provides a powerful CLI interface designed for both **AI agents** (default) and **humans** (`--readable`).

## 🚀 General Principles

- **Agent Mode (Default):** Outputs structured data using **TOON** or **Markdown**, optimized for token efficiency.
- **Human Mode (`--readable`):** Renders beautiful tables, panels, and colors using **Rich**.
- **FAIL FAST:** Errors are output as plain text to `stderr` with non-zero exit codes.

## 📂 Repository Scanning

Get a "Big Picture" view of a repository's structure, metadata, and recent activity.

```bash
# Agent Mode (TOON output)
gh-bridge scan owner/repo

# Human Mode (Visual report)
gh-bridge scan owner/repo --readable

# Scan a specific branch
gh-bridge scan owner/repo --branch develop --readable
```

## 🔍 Feature Tracing

Search for logic, keywords, or code snippets across multiple repositories.

```bash
# Search across multiple repos
gh-bridge trace "authentication" --repos "owner/repo1,owner/repo2"

# Human Mode with detailed matches
gh-bridge trace "manager" --readable
```

## 📊 Branch Analytics

Analyze branch health, commit trends, and contributor distribution.

```bash
# Default output
gh-bridge analyze-branch owner/repo main

# Human Mode
gh-bridge analyze-branch owner/repo main --readable
```

## 👤 User Activity Tracking

Trace a specific developer's recent work in a repository.

```bash
# Default output
gh-bridge trace-user username --repo owner/repo

# Human Mode
gh-bridge trace-user username --repo owner/repo --readable
```

## 🤖 PR Review

Generate an automated summary and review for a Pull Request.

```bash
# Agent Mode (Markdown output)
gh-bridge review-pr owner/repo 123

# Human Mode (Formatted Markdown)
gh-bridge review-pr owner/repo 123 --readable
```

## 🛠️ Global Options

- `--help`: Show available commands and options.
- `--readable`: Enable human-friendly output for any command.
- `GH_REPO` env var: Can be used as a fallback for repository selection.
