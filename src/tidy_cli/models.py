"""Typed data models shared between business logic and the CLI layer."""

from dataclasses import dataclass, field
from pathlib import Path


@dataclass(frozen=True)
class MoveAction:
    """Represents a single planned or executed file move."""

    source: Path
    destination: Path
    category: str
    renamed: bool = False


@dataclass
class OrganizePlan:
    """Result of scanning a directory before moving any files."""

    target_dir: Path
    actions: list[MoveAction] = field(default_factory=list)
    skipped_count: int = 0


@dataclass
class ExecutionResult:
    """Summary of an executed move or undo operation."""

    completed: list[MoveAction] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
    dry_run: bool = False
