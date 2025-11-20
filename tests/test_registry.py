import pytest
from knit.registry import register_extension, get_extension, clear_registry

@pytest.fixture(autouse=True)
def clean_registry():
    clear_registry()
    yield

def test_register_extension():
    @register_extension("TEST")
    def test_func(content, options, path):
        return "result"

    func = get_extension("TEST")
    assert func is test_func

def test_get_missing_extension():
    with pytest.raises(KeyError):
        get_extension("MISSING")

def test_register_duplicate_extension():
    @register_extension("TEST")
    def test_func1(content, options, path):
        return "1"

    # Should overwrite or raise warning? For now, let's assume overwrite is allowed but maybe we want to test behavior.
    # Let's just verify the second one is the one registered.
    @register_extension("TEST")
    def test_func2(content, options, path):
        return "2"
    
    assert get_extension("TEST") is test_func2
