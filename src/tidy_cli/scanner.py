"""Directory scanning and file classification logic (no console output)."""

from pathlib import Path

from tidy_cli.config import CATEGORY_EXTENSIONS, DEFAULT_CATEGORY
from tidy_cli.models import MoveAction, OrganizePlan


def classify_file(file_path: Path) -> str:
    """Return the category name for a file based on its lowercase extension."""
    extension = file_path.suffix.lower()
    for category, extensions in CATEGORY_EXTENSIONS.items():
        if extension in extensions:
            return category
    return DEFAULT_CATEGORY


def should_skip(entry: Path) -> bool:
    """Skip hidden entries, symlinks, and subdirectories for safety."""
    if entry.name.startswith("."):
        return True
    if entry.is_symlink():
        return True
    return not entry.is_file()


def resolve_unique_destination(
    destination: Path,
    reserved: set[Path],
) -> tuple[Path, bool]:
    """Avoid overwriting by adding an incremental numeric suffix if needed."""
    if not destination.exists() and destination not in reserved:
        return destination, False

    stem = destination.stem
    suffix = destination.suffix
    counter = 1
    while True:
        candidate = destination.with_name(f"{stem} ({counter}){suffix}")
        if not candidate.exists() and candidate not in reserved:
            return candidate, True
        counter += 1


def build_plan(target_dir: Path) -> OrganizePlan:
    """Scan target_dir and build a safe plan of file moves without touching disk."""
    plan = OrganizePlan(target_dir=target_dir)
    reserved: set[Path] = set()

    for entry in sorted(target_dir.iterdir(), key=lambda p: p.name.lower()):
        if should_skip(entry):
            plan.skipped_count += 1
            continue

        category = classify_file(entry)
        raw_destination = target_dir / category / entry.name
        final_destination, renamed = resolve_unique_destination(
            raw_destination, reserved
        )
        reserved.add(final_destination)

        plan.actions.append(
            MoveAction(
                source=entry,
                destination=final_destination,
                category=category,
                renamed=renamed,
            )
        )

    return plan
