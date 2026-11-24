# tidy-cli

A safe, fast Python CLI tool that automatically organizes files in any folder into clean category subfolders — with **dry-run previews**, **duplicate protection**, and **one-command undo**.

## Features

- **Smart categorization**: Groups files into `Documents`, `Images`, `Videos`, `Audio`, `Archives`, `Code`, `Installers`, and `Others` based on centralized rules in `src/tidy_cli/config.py`.
- **Dry-run mode (`--dry-run` / `-n`)**: Preview every planned move in a formatted table without touching a single file.
- **Duplicate protection**: Never overwrites existing files — automatically renames collisions with incremental suffixes (e.g. `report.pdf` → `report (1).pdf`).
- **Safe by design**: Never deletes user files or folders, and automatically skips hidden files (`.env`, `.git`), subdirectories, and symbolic links.
- **Undo support (`--undo`)**: Saves a `.tidy_history.json` log so you can revert the last run cleanly (even supporting `--undo --dry-run`).

## Tech Stack & Architecture

- **Python 3.10+** managed with [`uv`](https://docs.astral.sh/uv/) (`pyproject.toml` + `uv.lock`)
- **Typer** for CLI commands and argument validation
- **Rich** for clean terminal tables and styled output
- **pytest** for isolated automated tests (`tmp_path`)

```text
tidy-cli/
├── .agents/skills/          # Agent skills (architecture & file safety rules)
├── AGENTS.md                # Project-level rules
├── src/tidy_cli/
│   ├── main.py              # Presentation layer (Typer + Rich only)
│   ├── config.py            # Extension → category mapping
│   ├── models.py            # Typed dataclasses (MoveAction, OrganizePlan, ExecutionResult)
│   ├── scanner.py           # Pure scanning & classification logic
│   └── mover.py             # Safe file moves & JSON undo history
├── tests/
│   ├── test_scanner.py      # Scanner & duplicate-resolution tests
│   └── test_mover.py        # Dry-run, move, and undo roundtrip tests
└── pyproject.toml
```

## Installation

Make sure you have [`uv`](https://docs.astral.sh/uv/) installed, then clone and sync the project:

```bash
git clone https://github.com/DavidG-20/tidy-cli.git
cd tidy-cli
uv sync
```

## Usage

Preview changes without moving any files:

```bash
uv run tidy ~/Downloads --dry-run
```

Organize a folder:

```bash
uv run tidy ~/Downloads
```

Revert the last organization in that folder:

```bash
uv run tidy ~/Downloads --undo
```

Show help:

```bash
uv run tidy --help
```

## Running Tests

All tests run in isolated temporary directories (`pytest`'s `tmp_path` fixture):

```bash
uv run pytest -v
```

## License

MIT
