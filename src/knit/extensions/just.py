import re
from pathlib import Path
from knit.registry import register_extension

def get_just_recipe(justfile_path: Path, recipe_name: str) -> str:
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
    
    output_parts = []
    if doc_string:
        output_parts.append(doc_string)
        
    output_parts.append(f"```bash\njust {recipe_name}\n```")
    
    return "\n\n".join(output_parts)

@register_extension("JUST")
def just_extension(content: str, options: dict[str, str], file_path: Path) -> str:
    recipe = options.get("recipe")
    if not recipe:
        return "<!-- Error: 'recipe' option required -->"
        
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

    return get_just_recipe(justfile_path, recipe)
