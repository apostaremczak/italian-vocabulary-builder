install:
	uv sync --no-dev

install-dev:
	uv sync
	uv run pre-commit install
