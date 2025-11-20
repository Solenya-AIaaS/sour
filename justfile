set shell := ["zsh", "-c"]
UV_FLAGS := '--all-packages --all-groups'

[doc('List all available recipes')]
default:
    @just --list --unsorted

# ============================================================================
# 🛠️ Development
# ============================================================================

[doc('Install dependencies and sync environment')]
[group('dev')]
sync:
    uv sync --all-extras --all-groups

[doc('Run all tests')]
[group('dev')]
test:
    uv run {{ UV_FLAGS }} pytest

[doc('Lint and format code')]
[group('dev')]
lint:
    uv run {{ UV_FLAGS }} ruff check --fix
    uv run {{ UV_FLAGS }} ruff format

[doc('Check for dead code and complexity')]
[group('dev')]
check:
    uv run {{ UV_FLAGS }} vulture src tests
    uv run {{ UV_FLAGS }} complexipy src

# ============================================================================
# 📦 Build & Release
# ============================================================================

[doc('Build the package')]
[group('build')]
build:
    uv build

# ============================================================================
# 🧶 Knit
# ============================================================================

[doc('Run knit sync on the project documentation')]
[group('knit')]
knit:
    # Assuming knit is installed in the environment or run via python -m
    uv run knit sync README.md AGENTS.md DESIGN.md
