# Specification: User-Facing CLI Interface (Typer)

## Overview
Implement a robust, non-interactive CLI layer for `gh-bridge` using `Typer`. This interface will expose the existing Features Layer to both AI agents and human developers, prioritizing machine-readable output while providing high-quality "Rich" formatting for humans.

## Functional Requirements
- **Flat Command Structure**: Direct access to features via `gh-bridge <command>`.
- **Command Set**:
    - `scan`: Repository context analysis.
    - `trace`: Feature/code tracing.
    - `analyze-branch`: Branch analytics.
    - `review-pr`: PR review analysis.
    - `trace-user`: User activity tracking.
- **Agent-First Output Strategy**:
    - **Default**: Token-efficient, machine-readable formats:
        - **TOON**: `scan`, `trace`, `analyze-branch`, `trace-user` (optimized for structured data).
        - **Markdown**: `review-pr` (optimized for narrative prose).
    - **Human Override**: `--readable` flag enables `Rich` library rendering (tables, panels, colors, formatted markdown).
- **Format Support Matrix**:
    | Command        | Default Output | --readable Support        | Notes                     |
    |----------------|----------------|---------------------------|---------------------------|
    | `scan`         | TOON           | ✅ Rich tables/panels     | Large nested structures   |
    | `trace`        | TOON           | ✅ Rich tables/panels     | Cross-repo search results |
    | `analyze-branch`| TOON          | ✅ Rich tables/panels     | Branch statistics         |
    | `review-pr`    | Markdown       | ✅ Rich markdown rendering| Narrative prose           |
    | `trace-user`   | TOON           | ✅ Rich tables            | Simple commit list        |
- **Non-Interactive (Fail Fast)**: Immediate exit with error messages if required arguments are missing; no interactive prompts.

## Non-Functional Requirements
- **Performance**: Use lazy loading for subcommands to ensure fast startup times.
- **Typing**: Utilize `Annotated` types for clear, self-documenting CLI parameters.
- **Error Handling**:
    - Use `uv` Rich tracebacks globally for *uncaught* exceptions only.
    - User-facing errors (missing args, invalid input) must output plain text to `stderr` with non-zero exit code.
- **Architecture**:
    - Thin wrappers that delegate strictly to the Features Layer.
    - Use `@toon_unsupported` decorator to explicitly block TOON on incompatible commands.
    - Lazy imports inside command functions to optimize `gh-bridge --help` speed.

## Acceptance Criteria
- [ ] All 5 core features are accessible via the CLI.
- [ ] `gh-bridge --help` displays all commands and usage correctly.
- [ ] Missing required arguments trigger a non-zero exit code and error message.
- [ ] Default output matches the "Format Support Matrix" (TOON/Markdown).
- [ ] `--readable` flag produces high-quality terminal formatting.
- [ ] Unit tests verify CLI argument parsing, feature delegation, and correct output format selection.

## Out of Scope
- Global configuration files (e.g., `.gh-bridgerc`).
- Interactive prompts or setup wizards.
- Advanced caching or executor overrides (`--no-cache`, `--host`).
- Debug logging (`--debug`).
- Output file redirection (`--output`).
- Multiple format flags (`--json`, `--toon`, `--markdown` as separate flags).
