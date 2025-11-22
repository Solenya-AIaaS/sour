from collections.abc import Callable
from pathlib import Path

# Type alias for extension functions
ExtensionFunc = Callable[[str, dict[str, str], Path], str]

_EXTENSIONS: dict[str, ExtensionFunc] = {}

def register_extension(name: str) -> Callable[[ExtensionFunc], ExtensionFunc]:
    """Decorator to register a function as a knit extension."""
    def decorator(func: ExtensionFunc) -> ExtensionFunc:
        _EXTENSIONS[name] = func
        return func
    return decorator

def get_extension(name: str) -> ExtensionFunc:
    """Retrieve a registered extension by name."""
    if name not in _EXTENSIONS:
        raise KeyError(f"Extension '{name}' not found")
    return _EXTENSIONS[name]

def clear_registry() -> None:
    """Clear all registered extensions (useful for testing)."""
    _EXTENSIONS.clear()
