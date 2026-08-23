SOURCE = src main.py

run:
	@uv run main.py

install:
	@uv sync

lint:
	uv run flake8 $(SOURCE)
	uv run mypy $(SOURCE) \
	--warn-return-any \
	--warn-unused-ignores \
	--ignore-missing-imports \
	--disallow-untyped-defs \
	--check-untyped-defs

clean:
	@find . -type d -name "__pycache__" -exec rm -rf {} +
	@find . -type d -name ".mypy_cache" -exec rm -rf {} +
