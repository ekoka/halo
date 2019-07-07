import pytest
from halo.resource import Resource

def test_can_add_property():
    name = 'bar'
    r = Resource()
    r.prop(name, 'foo')
    assert r.document[name]=='foo'

def test_properties_with_reserved_word_raise_error():
    r = Resource()
    for name in ['_links', '_embedded']:
        with pytest.raises(ValueError) as e:
            r.prop(name, 'foo')
        assert 'reserved' in str(e.value).lower()

def test_can_delete_property():
    name = 'bar'
    r = Resource()
    r.prop(name, 'foo')
    r.delprop(name)
    assert name not in r.document
