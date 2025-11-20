import re
from pathlib import Path
from typing import Callable, Any

def parse_block(block: str) -> tuple[str, dict[str, str]]:
    """Parse a transform block header to extract name and options.
    
    Args:
        block: The block header string, e.g. '<!-- docs TREE path="." -->'
        
    Returns:
        Tuple of (transform_name, options_dict)
    """
    # Strip comment markers
    content = block.strip()
    if content.startswith("<!--"):
        content = content[4:]
    if content.endswith("-->"):
        content = content[:-3]
    content = content.strip()
    
    # Strip 'docs' prefix
    if content.startswith("docs"):
        content = content[4:].strip()
        
    parts = content.split(None, 1)
    name = parts[0]
    options = {}
    
    if len(parts) > 1:
        # Regex to match key="value", key='value', or key=value
        pattern = r'(\w+)=(?:"([^"]*)"|\'([^\']*)\'|(\S+))'
        for match in re.finditer(pattern, parts[1]):
            key = match.group(1)
            # Group 2 is double quoted, 3 is single quoted, 4 is unquoted
            val = match.group(2) if match.group(2) is not None else \
                  match.group(3) if match.group(3) is not None else \
                  match.group(4)
            options[key] = val
            
    return name, options

def process_content(
    content: str, 
    transform_func: Callable[[str, str, dict[str, str], Path], str],
    file_path: Path = Path("."),
) -> str:
    """Process markdown content and apply transforms.
    
    Args:
        content: The markdown content to process
        transform_func: Function to call for each block (name, current_body, options, path) -> new_content
        file_path: Path to the file being processed (for relative path resolution)
        
    Returns:
        Processed content
    """
    # Pattern to find blocks: <!-- docs NAME ... --> ... <!-- /docs -->
    pattern = r"(<!--\s*docs\s+([^>]+)\s*-->)(.*?)(<!--\s*/docs\s*-->)"
    
    def replacer(match: re.Match) -> str:
        header = match.group(1)
        current_body = match.group(3)
        footer = match.group(4)
        
        name, options = parse_block(header)
        
        try:
            new_body = transform_func(name, current_body, options, file_path)
            return f"{header}\n\n{new_body.strip()}\n\n{footer}"
        except Exception as e:
            return f"{header}\n\n<!-- Error: {str(e)} -->\n\n{footer}"

    return re.sub(pattern, replacer, content, flags=re.DOTALL)

def clear_content(content: str) -> str:
    """Clear content between transform blocks."""
    pattern = r"(<!--\s*docs\s+[^>]+\s*-->)(.*?)(<!--\s*/docs\s*-->)"
    return re.sub(pattern, r"\1\n\n<!-- /docs -->", content, flags=re.DOTALL)

