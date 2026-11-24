"""Safe file movement, duplicate renaming, and undo history persistence."""

from pathlib import Path
from tidy_cli.models import ExecutionResult, OrganizePlan


def execute_plan(plan: OrganizePlan, dry_run: bool = False) -> ExecutionResult:
    """Execute a planned set of moves, or return a preview if dry_run is True."""
    raise NotImplementedError("Mover logic will be implemented in the next step.")


def undo_last_run(target_dir: Path, dry_run: bool = False) -> ExecutionResult:
    """Revert the last recorded organization in target_dir using its history file."""
    raise NotImplementedError("Undo logic will be implemented in the next step.")
