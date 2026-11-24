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
    help="Organiza los archivos de una carpeta por categoría de forma segura (con --dry-run y --undo).",
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
    table.add_column("Origen", style="bold")
    table.add_column("Categoría", style="cyan")
    table.add_column("Destino", style="green")

    for action in actions:
        src_label = str(action.source.relative_to(target_dir))
        dest_rel = action.destination.relative_to(target_dir)
        dest_label = (
            f"{dest_rel} [yellow](renombrado)[/yellow]"
            if action.renamed
            else str(dest_rel)
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
            f"Vista previa de deshacer en {target}"
            if dry_run
            else f"Archivos restaurados en {target}"
        )
        _render_actions(result.completed, target, title)

    _render_errors(result)

    if dry_run and result.completed:
        console.print("[cyan]Modo simulación:[/cyan] no se movió ningún archivo.")
    elif result.completed:
        console.print(
            f"[green]Deshecho:[/green] se restauraron {len(result.completed)} archivo(s)."
        )

    if result.errors and not result.completed:
        raise typer.Exit(code=1)


def _handle_organize(plan: OrganizePlan, dry_run: bool) -> None:
    """Execute or preview an organization plan and print the summary."""
    if not plan.actions:
        console.print(
            f"[green]No hay archivos por organizar en {plan.target_dir}[/green] "
            f"(omitidos: {plan.skipped_count})."
        )
        return

    result = execute_plan(plan, dry_run=dry_run)
    title = (
        f"Vista previa (--dry-run) para {plan.target_dir}"
        if dry_run
        else f"Carpeta organizada: {plan.target_dir}"
    )
    _render_actions(result.completed, plan.target_dir, title)
    _render_errors(result)

    console.print(
        f"[dim]Procesados: {len(result.completed)} archivo(s) | "
        f"Omitidos (ocultos/carpetas/symlinks): {plan.skipped_count}[/dim]"
    )
    if dry_run:
        console.print("[cyan]Modo simulación:[/cyan] no se movió ningún archivo.")
    else:
        console.print(
            "[green]¡Listo![/green] Ejecuta con [bold]--undo[/bold] si quieres revertir."
        )

    if result.errors:
        raise typer.Exit(code=1)


@app.command()
def organize(
    target: Path = typer.Argument(
        ...,
        exists=True,
        file_okay=False,
        dir_okay=True,
        resolve_path=True,
        help="Ruta de la carpeta que deseas organizar.",
    ),
    dry_run: bool = typer.Option(
        False,
        "--dry-run",
        "-n",
        help="Muestra qué se movería sin tocar ningún archivo.",
    ),
    undo: bool = typer.Option(
        False,
        "--undo",
        help="Revierte el último ordenamiento realizado en esta carpeta.",
    ),
) -> None:
    """Organiza los archivos dentro de TARGET en subcarpetas por categoría."""
    if undo:
        _handle_undo(target, dry_run=dry_run)
        return

    plan = build_plan(target)
    _handle_organize(plan, dry_run=dry_run)


if __name__ == "__main__":
    app()
