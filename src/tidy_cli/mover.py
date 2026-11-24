"""Safe file movement, duplicate renaming, and undo history persistence."""

from datetime import datetime, timezone
import json
from pathlib import Path
import shutil

from tidy_cli.config import HISTORY_FILENAME
from tidy_cli.models import ExecutionResult, MoveAction, OrganizePlan
from tidy_cli.scanner import resolve_unique_destination


def _save_history(target_dir: Path, moves: list[MoveAction]) -> None:
    """Persist executed moves to a JSON file inside target_dir for --undo."""
    history_path = target_dir / HISTORY_FILENAME
    payload = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "moves": [
            {
                "source": str(move.source),
                "destination": str(move.destination),
                "category": move.category,
                "renamed": move.renamed,
            }
            for move in moves
        ],
    }
    history_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")


def _load_history(history_path: Path) -> list[dict[str, object]]:
    """Read recorded move entries from the history JSON file."""
    data = json.loads(history_path.read_text(encoding="utf-8"))
    moves = data.get("moves", [])
    if not isinstance(moves, list):
        raise ValueError("Invalid history file format.")
    return moves


def execute_plan(plan: OrganizePlan, dry_run: bool = False) -> ExecutionResult:
    """Execute a planned set of moves, or return a preview if dry_run is True."""
    if dry_run:
        return ExecutionResult(completed=list(plan.actions), dry_run=True)

    result = ExecutionResult(dry_run=False)
    reserved: set[Path] = set()

    for action in plan.actions:
        try:
            action.destination.parent.mkdir(parents=True, exist_ok=True)
            final_dest, extra_rename = resolve_unique_destination(
                action.destination, reserved
            )
            reserved.add(final_dest)
            shutil.move(str(action.source), str(final_dest))
            result.completed.append(
                MoveAction(
                    source=action.source,
                    destination=final_dest,
                    category=action.category,
                    renamed=action.renamed or extra_rename,
                )
            )
        except OSError as exc:
            result.errors.append(f"Failed to move {action.source.name}: {exc}")

    if result.completed:
        _save_history(plan.target_dir, result.completed)

    return result


def undo_last_run(target_dir: Path, dry_run: bool = False) -> ExecutionResult:
    """Revert the last recorded organization in target_dir using its history file."""
    history_path = target_dir / HISTORY_FILENAME
    result = ExecutionResult(dry_run=dry_run)

    if not history_path.exists():
        result.errors.append(f"No history file ({HISTORY_FILENAME}) found in {target_dir}.")
        return result

    try:
        entries = _load_history(history_path)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        result.errors.append(f"Could not read history file: {exc}")
        return result

    if not entries:
        result.errors.append("No moves recorded to undo.")
        return result

    reserved: set[Path] = set()
    for entry in reversed(entries):
        current_path = Path(str(entry["destination"]))
        original_path = Path(str(entry["source"]))
        category = str(entry.get("category", "Others"))

        if not current_path.exists():
            result.errors.append(f"Skipped missing file: {current_path}")
            continue

        restore_dest, renamed = resolve_unique_destination(original_path, reserved)
        reserved.add(restore_dest)

        if not dry_run:
            try:
                restore_dest.parent.mkdir(parents=True, exist_ok=True)
                shutil.move(str(current_path), str(restore_dest))
            except OSError as exc:
                result.errors.append(f"Failed to restore {current_path.name}: {exc}")
                continue

        result.completed.append(
            MoveAction(
                source=current_path,
                destination=restore_dest,
                category=category,
                renamed=renamed,
            )
        )

    if not dry_run and result.completed:
        _save_history(target_dir, [])

    return result
