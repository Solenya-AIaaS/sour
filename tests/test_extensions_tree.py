import pytest
from pathlib import Path
from sole.extensions.tree import generate_tree_content

@pytest.fixture
def temp_dir_structure(tmp_path):
    # Create a structure:
    # .
    # ├── dir1
    # │   ├── file1.txt
    # │   └── subdir
    # │       └── file2.txt
    # ├── dir2
    # └── file3.txt
    
    (tmp_path / "dir1" / "subdir").mkdir(parents=True)
    (tmp_path / "dir2").mkdir()
    (tmp_path / "dir1" / "file1.txt").touch()
    (tmp_path / "dir1" / "subdir" / "file2.txt").touch()
    (tmp_path / "file3.txt").touch()
    
    return tmp_path

def test_tree_basic(temp_dir_structure):
    output = generate_tree_content(temp_dir_structure, {"depth": "2"})
    assert "dir1" in output
    assert "file3.txt" in output
    assert "subdir" in output

def test_tree_depth(temp_dir_structure):
    output = generate_tree_content(temp_dir_structure, {"depth": "1"})
    assert "dir1" in output
    assert "dir2" in output
    assert "subdir" not in output

def test_tree_dirs_only(temp_dir_structure):
    output = generate_tree_content(temp_dir_structure, {"dirs_only": "true"})
    assert "dir1" in output
    assert "dir2" in output
    assert "file3.txt" not in output

def test_tree_exclude(temp_dir_structure):
    output = generate_tree_content(temp_dir_structure, {"exclude": "dir2"})
    assert "dir1" in output
    assert "dir2" not in output
