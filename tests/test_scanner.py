"""Unit tests for tidy_cli.scanner using pytest's isolated tmp_path fixture."""

from pathlib import Path

from tidy_cli.scanner import build_plan, classify_file


def test_classify_file_matches_case_insensitive_extensions() -> None:
    assert classify_file(Path("report.PDF")) == "Documents"
    assert classify_file(Path("photo.PNG")) == "Images"
    assert classify_file(Path("main.py")) == "Code"
    assert classify_file(Path("archive.tar.gz")) == "Archives"
    assert classify_file(Path("mystery.xyz")) == "Others"
    assert classify_file(Path("README")) == "Others"


def test_build_plan_skips_hidden_dirs_and_symlinks(tmp_path: Path) -> None:
    (tmp_path / "notes.txt").write_text("hello", encoding="utf-8")
    (tmp_path / ".secret").write_text("hidden", encoding="utf-8")
    (tmp_path / "subfolder").mkdir()
    (tmp_path / "link.txt").symlink_to(tmp_path / "notes.txt")

    plan = build_plan(tmp_path)

    assert len(plan.actions) == 1
    assert plan.actions[0].source.name == "notes.txt"
    assert plan.actions[0].category == "Documents"
    assert plan.skipped_count == 3


def test_build_plan_renames_duplicates_incrementally(tmp_path: Path) -> None:
    docs_dir = tmp_path / "Documents"
    docs_dir.mkdir()
    (docs_dir / "tarea.pdf").write_text("existing-1", encoding="utf-8")
    (docs_dir / "tarea (1).pdf").write_text("existing-2", encoding="utf-8")
    (tmp_path / "tarea.pdf").write_text("incoming", encoding="utf-8")

    plan = build_plan(tmp_path)

    assert len(plan.actions) == 1
    action = plan.actions[0]
    assert action.renamed is True
    assert action.destination == docs_dir / "tarea (2).pdf"
