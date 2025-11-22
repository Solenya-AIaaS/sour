import re
from pathlib import Path
from textwrap import dedent
from knit.registry import register_extension

def get_just_recipe(justfile_path: Path, recipe_name: str, format_str: str = "docs+command", quarto_safe: bool = False) -> str:
    """Extracts a recipe from a justfile and formats it for documentation.

    Args:
        justfile_path: Path to the justfile.
        recipe_name: Name of the recipe to extract.
        format_str: Comma or plus separated list of components to include.
            Options: "docs", "command", "code", "target_command".
            Aliases: "full" (docs+command), "doc" (docs).
        quarto_safe: If True, uses `{{bash}}` instead of `bash` for code fences.

    Returns:
        Formatted markdown string containing the requested recipe components.
    """
    if not justfile_path.exists():
        return f"<!-- Error: justfile not found at {justfile_path} -->"
        
    content = justfile_path.read_text()
    
    # Regex from example.py
    doc_pattern = rf"\[doc\('([^']+)'\)\](?:\s*\n\[group\([^\)]+\)\])?\s*\n{re.escape(recipe_name)}(?:\s|:)"
    recipe_pattern = rf"^{re.escape(recipe_name)}(?:\s+[^:\n]*)?:.*?(?=\n\n\[|^[a-z_]|\Z)"
    
    doc_match = re.search(doc_pattern, content, re.MULTILINE)
    recipe_match = re.search(recipe_pattern, content, re.MULTILINE | re.DOTALL)
    
    if not recipe_match:
        return f"<!-- Error: Recipe '{recipe_name}' not found in justfile -->"
        
    doc_string = doc_match.group(1) if doc_match else None
    recipe_code = recipe_match.group(0).strip()
    
    # Extract target_command (body)
    lines = recipe_code.splitlines()
    if len(lines) > 1:
        # Join lines after the first one and dedent
        body = "\n".join(lines[1:])
        target_command = dedent(body).strip()
    else:
        target_command = ""

    # Parse formats
    # Normalize separators and split
    raw_formats = format_str.replace("+", ",").split(",")
    formats = set(f.strip() for f in raw_formats)
    
    # Aliases
    if "full" in formats:
        formats.remove("full")
        formats.add("docs")
        formats.add("command")
    if "doc" in formats:
        formats.remove("doc")
        formats.add("docs")

    # Determine code fence syntax based on quarto_safe option
    bash_fence = "```{{bash}}" if quarto_safe else "```bash"
    just_fence = "```{{just}}" if quarto_safe else "```just"

    output_parts = []

    # 1. docs
    if "docs" in formats:
        if doc_string:
            output_parts.append(doc_string)
        # We don't error if missing, just skip

    # 2. command
    if "command" in formats:
        output_parts.append(f"{bash_fence}\njust {recipe_name}\n```")

    # 3. code
    if "code" in formats:
        output_parts.append(f"{just_fence}\n{recipe_code}\n```")

    # 4. target_command
    if "target_command" in formats:
        if target_command:
            output_parts.append(f"{bash_fence}\n{target_command}\n```")

    return "\n\n".join(output_parts)

@register_extension("JUST")
def just_extension(content: str, options: dict[str, str], file_path: Path) -> str:
    """Knit extension to include recipes from a justfile.

    Args:
        content: The existing content within the block (ignored).
        options: Dictionary of options from the block header.
            - recipe: Name of the recipe (required).
            - format: Output format (default: "docs+command").
            - quarto_safe: "true" or "false" (default: "false").
        file_path: Path to the markdown file being processed.

    Returns:
        The generated markdown content.
    """
    recipe = options.get("recipe")
    if not recipe:
        return "<!-- Error: 'recipe' option required -->"
    
    output_format = options.get("format", "docs+command")
    quarto_safe = options.get("quarto_safe", "false").lower() == "true"
        
    # Find justfile
    # Try same dir, then parent, then root
    candidates = [
        file_path.parent / "justfile",
        file_path.parent.parent / "justfile",
        Path("justfile")
    ]
    
    justfile_path = None
    for p in candidates:
        if p.exists():
            justfile_path = p
            break
            
    if not justfile_path:
        # For testing purposes, if we can't find it, we might want to pass the path directly?
        # The test `test_justfile_not_found` expects a specific error.
        # Let's default to one of them for the error message
        justfile_path = file_path.parent / "justfile"

    return get_just_recipe(justfile_path, recipe, output_format, quarto_safe)
