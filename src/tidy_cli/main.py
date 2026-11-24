"""CLI entry point for tidy-cli (presentation layer using Typer + Rich)."""

from pathlib import Path

import typer
from rich.console import Console
from rich.table import Table

from tidy_cli.models import OrganizePlan
from tidy_cli.scanner import build_plan

app = typer.Typer(
    name="tidy",
    help="Organize files in a folder by category safely (with --dry-run and --undo).",
    no_args_is_help=True,
)
console = Console()


def _render_plan(plan: OrganizePlan, dry_run: bool) -> None:
    """Display the planned moves in a clean Rich table."""
    title = (
        f"Dry-run preview for {plan.target_dir}"
        if dry_run
        else f"Organization plan for {plan.target_dir}"
    )
    table = Table(title=title, show_lines=False)
    table.add_column("File", style="bold")
    table.add_column("Category", style="cyan")
    table.add_column("Destination", style="green")

    for action in plan.actions:
        rel_dest = action.destination.relative_to(plan.target_dir)
        dest_label = f"{rel_dest} [yellow](renamed)[/yellow]" if action.renamed else str(rel_dest)
        table.add_row(action.source.name, action.category, dest_label)

    console.print(table)
    console.print(
        f"[dim]Planned: {len(plan.actions)} file(s) | "
        f"Skipped (hidden/dirs/symlinks): {plan.skipped_count}[/dim]"
    )


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
        console.print("[yellow]Undo logic will be implemented in the next step.[/yellow]")
        return

    plan = build_plan(target)
    if not plan.actions:
        console.print(
            f"[green]Nothing to organize in {target}[/green] "
            f"(skipped: {plan.skipped_count})."
        )
        return

    _render_plan(plan, dry_run=dry_run)

    if dry_run:
        console.print("[cyan]Dry-run mode:[/cyan] no files were moved.")
        return

    console.print("[yellow]Mover logic will be connected in the next step.[/yellow]")


if __name__ == "__main__":
    app()
