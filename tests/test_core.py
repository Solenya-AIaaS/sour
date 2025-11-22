from knit.core import parse_block, process_content

def test_parse_block_simple():
    block = '<!-- docs TREE path="." -->'
    name, options = parse_block(block)
    assert name == "TREE"
    assert options == {"path": "."}

def test_parse_block_multiple_options():
    block = '<!-- docs TREE path="." depth=2 dirs_only=true -->'
    name, options = parse_block(block)
    assert name == "TREE"
    assert options == {"path": ".", "depth": "2", "dirs_only": "true"}

def test_parse_block_quoted_values():
    block = '<!-- docs HELLO message="Hello World" -->'
    name, options = parse_block(block)
    assert name == "HELLO"
    assert options == {"message": "Hello World"}

def test_process_content_no_blocks():
    content = "# Title\n\nSome text."
    new_content = process_content(content, lambda n, o, p: "")
    assert new_content == content

def test_process_content_with_block():
    content = """
# Title

<!-- docs TEST key="value" -->
Old Content
<!-- /docs -->
"""
    expected = """
# Title

<!-- docs TEST key="value" -->

New Content

<!-- /docs -->
"""
    
    def mock_transform(name, body, options, file_path):
        assert name == "TEST"
        assert options == {"key": "value"}
        return "New Content"

    new_content = process_content(content, mock_transform)
    assert new_content.strip() == expected.strip()
