import typer
from rich.console import Console

app = typer.Typer(help="Knit: Auto-sync dynamic content in markdown files")
console = Console()

@app.callback()
def callback():
    """
    Knit: A tool for maintaining dynamic markdown documentation.
    """
    pass

@app.command()
def version():
    """Show the version of knit."""
    from knit import __version__
    console.print(f"Knit version: {__version__}")

if __name__ == "__main__":
    app()
