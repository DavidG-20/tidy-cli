"""Unit tests for tidy_cli.mover (execution, dry-run, and undo) using tmp_path."""

from pathlib import Path

from tidy_cli.config import HISTORY_FILENAME
from tidy_cli.mover import execute_plan, undo_last_run
from tidy_cli.scanner import build_plan


def test_execute_plan_dry_run_does_not_touch_disk(tmp_path: Path) -> None:
    sample = tmp_path / "photo.jpg"
    sample.write_text("img", encoding="utf-8")

    plan = build_plan(tmp_path)
    result = execute_plan(plan, dry_run=True)

    assert result.dry_run is True
    assert len(result.completed) == 1
    assert sample.exists()
    assert not (tmp_path / "Images").exists()
    assert not (tmp_path / HISTORY_FILENAME).exists()


def test_execute_plan_and_undo_roundtrip(tmp_path: Path) -> None:
    docs_dir = tmp_path / "Documents"
    docs_dir.mkdir()
    (docs_dir / "tarea.pdf").write_text("original-in-docs", encoding="utf-8")
    (tmp_path / "tarea.pdf").write_text("new-tarea", encoding="utf-8")
    (tmp_path / "app.py").write_text("print('hi')", encoding="utf-8")

    plan = build_plan(tmp_path)
    exec_result = execute_plan(plan, dry_run=False)

    assert not exec_result.errors
    assert len(exec_result.completed) == 2
    assert (docs_dir / "tarea.pdf").read_text(encoding="utf-8") == "original-in-docs"
    assert (docs_dir / "tarea (1).pdf").read_text(encoding="utf-8") == "new-tarea"
    assert (tmp_path / "Code" / "app.py").exists()
    assert (tmp_path / HISTORY_FILENAME).exists()

    undo_result = undo_last_run(tmp_path, dry_run=False)

    assert not undo_result.errors
    assert len(undo_result.completed) == 2
    assert (tmp_path / "tarea.pdf").read_text(encoding="utf-8") == "new-tarea"
    assert (tmp_path / "app.py").exists()
    assert (docs_dir / "tarea.pdf").read_text(encoding="utf-8") == "original-in-docs"

    second_undo = undo_last_run(tmp_path, dry_run=False)
    assert not second_undo.completed
    assert second_undo.errors


def test_undo_without_history_returns_clear_error(tmp_path: Path) -> None:
    result = undo_last_run(tmp_path)
    assert not result.completed
    assert len(result.errors) == 1
    assert HISTORY_FILENAME in result.errors[0]


def test_undo_does_not_overwrite_new_file_at_original_path(tmp_path: Path) -> None:
    (tmp_path / "script.py").write_text("old-version", encoding="utf-8")

    plan = build_plan(tmp_path)
    execute_plan(plan, dry_run=False)

    # User creates a brand-new file with the same name before running --undo
    (tmp_path / "script.py").write_text("brand-new", encoding="utf-8")

    undo_result = undo_last_run(tmp_path, dry_run=False)

    assert not undo_result.errors
    assert (tmp_path / "script.py").read_text(encoding="utf-8") == "brand-new"
    assert (tmp_path / "script (1).py").read_text(encoding="utf-8") == "old-version"
