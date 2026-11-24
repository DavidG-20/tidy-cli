"""Directory scanning and file classification logic (no console output)."""

from pathlib import Path
from tidy_cli.models import OrganizePlan


def build_plan(target_dir: Path) -> OrganizePlan:
    """Scan target_dir and build a safe plan of file moves without touching disk."""
    raise NotImplementedError("Scanner logic will be implemented in the next step.")
