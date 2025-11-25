from pathlib import Path
import yaml
from sole.registry import register_extension

def find_readme_descriptions(root: Path) -> dict[str, str]:
    """Find all README.md files and extract directory descriptions from YAML frontmatter.
    
    Args:
        root: The root directory to search from.

    Returns:
        A dictionary mapping relative directory paths to their descriptions.
    """
    descriptions = {}
    for readme in root.rglob("README.md"):
        try:
            content = readme.read_text()
            if content.startswith("---\n"):
                parts = content.split("---\n", 2)
                if len(parts) >= 3:
                    frontmatter = yaml.safe_load(parts[1]) or {}
                    if "description" in frontmatter:
                        rel_path = readme.parent.relative_to(root)
                        descriptions[str(rel_path)] = frontmatter["description"]
        except Exception:
            pass
    return descriptions

def generate_tree(
    directory: Path,
    prefix: str = "",
    max_depth: int = 1,
    current_depth: int = 0,
    exclude_patterns: list[str] | None = None,
    include_hidden: bool = False,
    dirs_only: bool = False,
) -> list[tuple[str, Path]]:
    """Recursively generates a directory tree structure.

    Args:
        directory: The directory to traverse.
        prefix: The prefix string for the current line (used for indentation).
        max_depth: Maximum depth to traverse.
        current_depth: Current depth in the traversal.
        exclude_patterns: List of glob patterns to exclude.
        include_hidden: Whether to include hidden files/directories.
        dirs_only: Whether to list only directories.

    Returns:
        A list of tuples, where each tuple contains:
        - The formatted tree line string.
        - The absolute Path object corresponding to that line.
    """
    if exclude_patterns is None:
        exclude_patterns = []

    if current_depth >= max_depth:
        return []

    lines = []
    try:
        items = sorted(directory.iterdir(), key=lambda p: (not p.is_dir(), p.name))
        filtered_items = []
        for item in items:
            if not include_hidden and item.name.startswith("."):
                continue
            if dirs_only and not item.is_dir():
                continue
            
            should_exclude = False
            for pattern in exclude_patterns:
                if item.match(pattern) or item.name == pattern:
                    should_exclude = True
                    break
            if not should_exclude:
                filtered_items.append(item)
        
        items = filtered_items

        for i, item in enumerate(items):
            is_last = i == len(items) - 1
            connector = "└── " if is_last else "├── "
            extension = "    " if is_last else "│   "
            
            lines.append((f"{prefix}{connector}{item.name}", item))
            
            if item.is_dir() and current_depth + 1 < max_depth:
                lines.extend(
                    generate_tree(
                        item,
                        prefix + extension,
                        max_depth,
                        current_depth + 1,
                        exclude_patterns,
                        include_hidden,
                        dirs_only,
                    )
                )
    except PermissionError:
        pass
    return lines

def generate_tree_content(directory: Path, options: dict[str, str]) -> str:
    """Generate the tree content string based on options.
    
    Args:
        directory: The base directory to generate the tree from.
        options: Dictionary of options.
            - path: Relative path to start tree from (default: ".").
            - depth: Max depth (default: "1").
            - dirs_only: "true" or "false" (default: "false").
            - add_docs: "true" or "false" (default: "true").
            - exclude: Comma-separated list of patterns to exclude.

    Returns:
        The generated tree string, optionally annotated with descriptions.
    """
    path_str = options.get("path", ".")
    depth = int(options.get("depth", "1"))
    dirs_only = options.get("dirs_only", "false").lower() == "true"
    add_docs = options.get("add_docs", "true").lower() == "true"
    exclude = options.get("exclude", "").split(",") if options.get("exclude") else []
    exclude = [p.strip() for p in exclude if p.strip()]
    
    target_dir = directory / path_str
    if not target_dir.exists():
        return f"Error: Directory not found: {target_dir}"
        
    tree_items = [(path_str, target_dir)]
    tree_items.extend(
        generate_tree(target_dir, "", depth, 0, exclude, False, dirs_only)
    )
    
    # Load descriptions from README.md files
    descriptions = find_readme_descriptions(directory) if add_docs else {}

    # Annotate tree with descriptions
    annotated_lines = []

    for line, item_path in tree_items:
        try:
            rel_path = item_path.relative_to(directory)
            lookup_path = str(rel_path)
            
            if add_docs and lookup_path in descriptions:
                annotated_lines.append(f"{line} # {descriptions[lookup_path]}")
            else:
                annotated_lines.append(line)
        except ValueError:
            annotated_lines.append(line)

    return "\n".join(annotated_lines)

# This function matches the signature expected by the registry
@register_extension("TREE")
def tree_extension(content: str, options: dict[str, str], file_path: Path) -> str:
    """Sole extension to generate a directory tree.

    Args:
        content: The existing content within the block (ignored).
        options: Dictionary of options from the block header.
        file_path: Path to the markdown file being processed.

    Returns:
        The generated markdown content wrapped in a code block.
    """
    # content is the existing content inside the block (unused for tree usually)
    # file_path is the path of the markdown file
    return f"```\n{generate_tree_content(file_path.parent, options)}\n```"
