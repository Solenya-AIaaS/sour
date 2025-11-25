import typer
from pathlib import Path
from typing import Annotated
from rich.console import Console

from sole import __version__
from sole.core import process_content, clear_content
from sole.registry import get_extension
# Importing these modules registers the extensions via decorators
import sole.extensions.tree
import sole.extensions.just

app = typer.Typer(help="Sole: Auto-sync dynamic content in markdown files")
console = Console()

def load_extensions():
    # Built-ins are registered on import
    # TODO: Load custom extensions from pyproject.toml
    pass


@app.callback()
def callback():
    """
    Sole: A tool for maintaining dynamic markdown documentation.
    """
    load_extensions()


@app.command()
def version():
    """Show the version of sole."""
    console.print(f"Sole version: {__version__}")


@app.command()
def sync(
    files: Annotated[list[Path] | None, typer.Argument(help="Markdown files or directories to process")] = None,
    check: Annotated[bool, typer.Option("--check", help="Dry-run: check if files would be modified")] = False,
    verbose: Annotated[bool, typer.Option("--verbose", "-v", help="Show detailed output")] = False,
):
    """Auto-sync dynamic content in markdown files."""
    target_paths = files if files else [Path(".")]
    files_to_process = set()

    for path in target_paths:
        if not path.exists():
            console.print(f"[red]Error: Path not found: {path}[/red]")
            continue
        
        if path.is_file():
            files_to_process.add(path)
        elif path.is_dir():
            files_to_process.update(path.rglob("*.md"))
            files_to_process.update(path.rglob("*.qmd"))

    if not files_to_process:
        console.print("[yellow]No files found to process.[/yellow]")
        raise typer.Exit(0)

    modified_files = []

    def transform_resolver(name: str, body: str, options: dict[str, str], path: Path) -> str:
        try:
            func = get_extension(name)
            return func(body, options, path)
        except KeyError:
             console.print(f"[yellow]Warning: Unknown extension '{name}' in {path}[/yellow]")
             raise

    for file_path in sorted(files_to_process):
        if verbose:
            console.print(f"[cyan]Processing {file_path}...[/cyan]")

        original_content = file_path.read_text()
        new_content = process_content(original_content, transform_resolver, file_path)

        if new_content != original_content:
            modified_files.append(file_path)
            if check:
                console.print(f"[yellow]Would modify: {file_path}[/yellow]")
            else:
                file_path.write_text(new_content)
                console.print(f"[green]✓ Updated {file_path}[/green]")
        else:
            if verbose:
                console.print(f"[dim]  No changes needed for {file_path}[/dim]")

    # Summary
    console.print()
    console.print("[bold]Results:[/bold]")
    console.print(f"  Files processed: {len(files_to_process)}")
    console.print(f"  Files modified: {len(modified_files)}")

    if check and modified_files:
        console.print()
        console.print("[yellow]Run without --check to apply changes[/yellow]")
        raise typer.Exit(1)

    if not check and modified_files:
        console.print()
        console.print("[green]✓ All transforms applied successfully[/green]")

@app.command()
def clear(
    files: Annotated[list[Path] | None, typer.Argument(help="Markdown files or directories to clear")] = None,
    check: Annotated[bool, typer.Option("--check", help="Dry-run: check what would be cleared")] = False,
):
    """Clear all content between transform comment blocks."""
    target_paths = files if files else [Path(".")]
    files_to_process = set()

    for path in target_paths:
        if not path.exists():
            console.print(f"[red]Error: Path not found: {path}[/red]")
            continue
        
        if path.is_file():
            files_to_process.add(path)
        elif path.is_dir():
            files_to_process.update(path.rglob("*.md"))
            files_to_process.update(path.rglob("*.qmd"))

    if not files_to_process:
        console.print("[yellow]No files found to process.[/yellow]")
        raise typer.Exit(0)

    modified_files = []

    for file_path in sorted(files_to_process):
        content = file_path.read_text()
        new_content = clear_content(content)

        if new_content != content:
            modified_files.append(file_path)
            if check:
                console.print(f"[yellow]Would clear: {file_path}[/yellow]")
            else:
                file_path.write_text(new_content)
                console.print(f"[green]✓ Cleared {file_path}[/green]")
        else:
            console.print(f"[dim]No transform blocks found in {file_path}[/dim]")

    # Summary
    console.print()
    if check and modified_files:
        console.print("[yellow]Run without --check to apply changes[/yellow]")
    elif not check and modified_files:
        console.print("[green]✓ All blocks cleared successfully[/green]")
    else:
        console.print("[dim]No changes needed[/dim]")

if __name__ == "__main__":
    app()
