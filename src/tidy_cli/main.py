"""CLI entry point for tidy-cli (presentation layer using Typer + Rich)."""

from pathlib import Path

import typer
from rich.console import Console
from rich.table import Table

from tidy_cli.models import ExecutionResult, MoveAction, OrganizePlan
from tidy_cli.mover import execute_plan, undo_last_run
from tidy_cli.scanner import build_plan

app = typer.Typer(
    name="tidy",
    help="Organize files in a folder by category safely (with --dry-run and --undo).",
    no_args_is_help=True,
)
console = Console()


def _render_actions(
    actions: list[MoveAction],
    target_dir: Path,
    title: str,
) -> None:
    """Display planned or completed moves in a Rich table."""
    table = Table(title=title, show_lines=False)
    table.add_column("From", style="bold")
    table.add_column("Category", style="cyan")
    table.add_column("To", style="green")

    for action in actions:
        src_label = str(action.source.relative_to(target_dir))
        dest_rel = action.destination.relative_to(target_dir)
        dest_label = (
            f"{dest_rel} [yellow](renamed)[/yellow]" if action.renamed else str(dest_rel)
        )
        table.add_row(src_label, action.category, dest_label)

    console.print(table)


def _render_errors(result: ExecutionResult) -> None:
    """Print any non-fatal errors returned by the mover."""
    for error in result.errors:
        console.print(f"[red]Error:[/red] {error}")


def _handle_undo(target: Path, dry_run: bool) -> None:
    """Execute or preview --undo and print the summary."""
    result = undo_last_run(target, dry_run=dry_run)
    if result.completed:
        title = (
            f"Undo dry-run preview for {target}"
            if dry_run
            else f"Restored files in {target}"
        )
        _render_actions(result.completed, target, title)

    _render_errors(result)

    if dry_run and result.completed:
        console.print("[cyan]Dry-run mode:[/cyan] no files were moved.")
    elif result.completed:
        console.print(f"[green]Undone:[/green] restored {len(result.completed)} file(s).")


def _handle_organize(plan: OrganizePlan, dry_run: bool) -> None:
    """Execute or preview an organization plan and print the summary."""
    if not plan.actions:
        console.print(
            f"[green]Nothing to organize in {plan.target_dir}[/green] "
            f"(skipped: {plan.skipped_count})."
        )
        return

    result = execute_plan(plan, dry_run=dry_run)
    title = (
        f"Dry-run preview for {plan.target_dir}"
        if dry_run
        else f"Organized {plan.target_dir}"
    )
    _render_actions(result.completed, plan.target_dir, title)
    _render_errors(result)

    console.print(
        f"[dim]Processed: {len(result.completed)} file(s) | "
        f"Skipped (hidden/dirs/symlinks): {plan.skipped_count}[/dim]"
    )
    if dry_run:
        console.print("[cyan]Dry-run mode:[/cyan] no files were moved.")
    else:
        console.print("[green]Done![/green] Run with [bold]--undo[/bold] to revert.")


@app.command()
def organize(
    target: Path = typer.Argument(
        ...,
        exists=True,
        file_okay=False,
        dir_okay=True,
        resolve_path=True,
        help="Path to the folder you want to organize.",
    ),
    dry_run: bool = typer.Option(
        False,
        "--dry-run",
        "-n",
        help="Preview what would be moved without touching any files.",
    ),
    undo: bool = typer.Option(
        False,
        "--undo",
        help="Revert the last organization performed in this folder.",
    ),
) -> None:
    """Organize files inside TARGET into category subfolders."""
    if undo:
        _handle_undo(target, dry_run=dry_run)
        return

    plan = build_plan(target)
    _handle_organize(plan, dry_run=dry_run)


if __name__ == "__main__":
    app()
