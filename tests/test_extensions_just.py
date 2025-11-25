import pytest
from sole.extensions.just import get_just_recipe

@pytest.fixture
def justfile_content(tmp_path):
    content = """
# Some comment
[doc('Run tests')]
test:
    pytest

[doc('Build project')]
build:
    uv build
"""
    f = tmp_path / "justfile"
    f.write_text(content)
    return f

def test_get_recipe_simple(justfile_content):
    recipe = get_just_recipe(justfile_content, "test")
    assert "Run tests" in recipe
    # assert "pytest" in recipe # Default format does not include recipe body
    assert "```bash" in recipe
    assert "just test" in recipe

def test_get_recipe_missing(justfile_content):
    recipe = get_just_recipe(justfile_content, "missing")
    assert "Recipe 'missing' not found" in recipe

def test_justfile_not_found(tmp_path):
    recipe = get_just_recipe(tmp_path / "nonexistent", "test")
    assert "justfile not found" in recipe

def test_get_recipe_formats(justfile_content):
    # Test docs+target_command
    recipe = get_just_recipe(justfile_content, "build", format_str="docs+target_command")
    assert "Build project" in recipe
    assert "uv build" in recipe
    assert "just build" not in recipe

    # Test command only
    recipe = get_just_recipe(justfile_content, "test", format_str="command")
    assert "Run tests" not in recipe
    assert "just test" in recipe
