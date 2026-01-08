# Product Guidelines

## Output Tone & Voice
- **Succinct & Machine-Readable:** All primary outputs intended for AI agents must prioritize token efficiency and strict JSON validity. Avoid unnecessary prose or decorative formatting in data payloads.

## Error Handling
- **Standardized Error Envelopes:** Every response from the system must follow a consistent structure. Errors must be returned as JSON objects containing an `error` field, a status code (if applicable), and a concise, actionable error message to allow agents to recover or report issues programmatically.

## Feature Design Philosophy
- **Compositional Architecture:** New high-level features should be built by composing existing low-level command wrappers. This ensures consistency in how the GitHub CLI is invoked and data is processed, while maximizing code reuse across the `gh_wrapper.features` module.

## Performance
- **Minimal Latency:** Features should be optimized for speed, as agents often operate in real-time loops. Use caching where appropriate to avoid redundant CLI calls.
