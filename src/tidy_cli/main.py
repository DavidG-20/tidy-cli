"""CLI entry point for tidy-cli (presentation layer using Typer + Rich)."""

from pathlib import Path
import typer
from rich.console import Console

app = typer.Typer(
    name="tidy",
    help="Organize files in a folder by category safely (with --dry-run and --undo).",
    no_args_is_help=True,
)
console = Console()


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
    console.print(
        f"[cyan]tidy-cli skeleton ready[/cyan] -> target: [bold]{target}[/bold] "
        f"(dry_run={dry_run}, undo={undo})"
    )
    console.print("[yellow]Next step:[/yellow] implement scanner and mover logic.")


if __name__ == "__main__":
    app()
