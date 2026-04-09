# Default recipe
default:
    @just --list

# Scrape a HelloFresh recipe URL and export as YAML
scrape url:
    cd src && ../.venv/bin/python -m scraper "{{url}}"

# Run tests
test *args:
    .venv/bin/python -m pytest {{args}}

# Install dependencies into .venv
install:
    uv venv .venv
    uv pip install -e ".[dev]" --python .venv/bin/python

# Run linter
lint:
    .venv/bin/python -m pytest --co -q
