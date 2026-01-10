# Plan: User-Facing CLI Interface (Typer)

## File Ownership Assignment
| Agent | Domain | Directory/Files |
| :--- | :--- | :--- |
| **Agent A** (Core) | Foundational CLI Infrastructure | `src/gh_wrapper/utils/cli_helpers.py`, `src/gh_wrapper/main.py` (entry point setup) |
| **Agent B** (Feature) | CLI Implementation & Formatting | `src/gh_wrapper/cli/`, `tests/unit/test_cli.py`, `tests/integration/test_cli_integration.py` |

---

## Phase 1: Foundation & CLI Infrastructure
- [] **[Agent A]** Task: Add `typer` and `toon-format` dependencies to `pyproject.toml`.
- [] **[Agent A]** Task: Define the base CLI entry point in `pyproject.toml` (script entry point `gh-bridge`).
- [] **[Agent A]** Task: Initialize CLI package structure and `Typer` app in `src/gh_wrapper/cli/`.
- [] **[Agent A]** Task: Implement `@toon_unsupported` decorator and lazy-loading infrastructure in `src/gh_wrapper/utils/cli_helpers.py`.
- [] **[Agent A]** Task: Configure global `Rich` traceback handling in the main entry point.
- [] **[Agent B]** Task: Create initial unit test suite for CLI argument parsing.
- [] Task: Conductor - User Manual Verification 'Phase 1: Foundation' (Protocol in workflow.md)

## Phase 2: Implementation of Data-Heavy Commands (TOON)
- [] **[Agent B]** Task: Implement `scan` command with TOON default and Rich human override.
- [] **[Agent B]** Task: Implement `trace` command with TOON default and Rich human override.
- [] **[Agent B]** Task: Implement `analyze-branch` command with TOON default and Rich human override.
- [] **[Agent B]** Task: Implement `trace-user` command with TOON default and Rich human override.
- [] **[Agent B]** Task: Verify TOON output formats match specification requirements.
- [] Task: Conductor - User Manual Verification 'Phase 2: Data-Heavy Commands' (Protocol in workflow.md)

## Phase 3: Implementation of Prose Commands (Markdown)
- [] **[Agent B]** Task: Implement `review-pr` command with Markdown default and Rich human override.
- [] **[Agent B]** Task: Apply `@toon_unsupported` decorator to `review-pr` to ensure correct error handling.
- [] **[Agent B]** Task: Verify Markdown rendering consistency across agents and humans.
- [] Task: Conductor - User Manual Verification 'Phase 3: Prose Commands' (Protocol in workflow.md)

## Phase 4: Error Handling & Optimization
- [] **[Agent A]** Task: Refine "Fail Fast" logic to ensure non-interactive behavior and plain-text stderr for user errors.
- [] **[Agent A]** Task: Finalize lazy loading imports inside all command functions to optimize `--help` performance.
- [] **[Agent B]** Task: Implement comprehensive error handling for network/CLI failures within the CLI layer.
- [] Task: Conductor - User Manual Verification 'Phase 4: Error Handling' (Protocol in workflow.md)

## Phase 5: Final Integration & Coverage
- [] **[Agent B]** Task: Complete integration tests for all CLI commands using real/mocked GH outputs.
- [] **[Agent B]** Task: Verify unit test coverage is >80% for the new CLI modules.
- [] **[Agent B]** Task: Update `README.md` with CLI usage examples for all commands.
- [] **[Agent B]** Task: Add CLI section to documentation showing both agent (default) and human (`--readable`) modes.
- [] **[Agent B]** Task: Perform final end-to-end "smoke tests" for both Agent (default) and Human (`--readable`) modes.
- [] Task: Conductor - User Manual Verification 'Phase 5: Final Integration' (Protocol in workflow.md)
