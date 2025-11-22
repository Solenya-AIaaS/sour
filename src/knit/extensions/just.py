import re
from pathlib import Path
from knit.registry import register_extension

def get_just_recipe(justfile_path: Path, recipe_name: str, format: str = "full", quarto_safe: bool = False) -> str:
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
    
    # Determine code fence syntax based on quarto_safe option
    bash_fence = "```{{bash}}" if quarto_safe else "```bash"
    just_fence = "```{{just}}" if quarto_safe else "```just"

    # Generate output based on format
    if format == "doc":
        if doc_string:
            return doc_string
        return f"<!-- No doc string found for recipe '{recipe_name}' -->"

    elif format == "command":
        return f"{bash_fence}\njust {recipe_name}\n```"

    elif format == "code":
        return f"{just_fence}\n{recipe_code}\n```"

    else:  # full
        output_parts = []
        if doc_string:
            output_parts.append(doc_string)
        output_parts.append(f"{bash_fence}\njust {recipe_name}\n```")
        return "\n\n".join(output_parts)

@register_extension("JUST")
def just_extension(content: str, options: dict[str, str], file_path: Path) -> str:
    recipe = options.get("recipe")
    if not recipe:
        return "<!-- Error: 'recipe' option required -->"
    
    output_format = options.get("format", "full")
    if output_format not in ("full", "doc", "command", "code"):
        return f"<!-- Error: Invalid format '{output_format}'. Use: full, doc, command, or code -->"

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
