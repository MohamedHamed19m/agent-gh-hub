#!/bin/bash
# scripts/setup_dev.sh

# Install uv
curl -LsSf https://astral.sh/uv/install.sh | sh

# Sync dependencies
uv sync --all-extras

# Setup pre-commit
uv run pre-commit install

echo "Development environment setup complete!"
