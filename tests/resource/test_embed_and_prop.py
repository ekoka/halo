import pytest
from halo.resource import Resource

def test_can_add_property():
    name = 'bar'
    r = Resource()
    r.addprop(name, 'foo')
    assert r.document[name]=='foo'

def test_can_return_property():
    name = 'bar'
    r = Resource()
    r.addprop(name, 'foo')
    assert r.getprop(name)=='foo'

def test_return_undefined_property_raise_error():
    r = Resource()
    with pytest.raises(KeyError) as e:
        r.getprop('foo')
    assert 'not found' in str(e.value).lower()

def test_add_reserved_properties_raise_error():
    r = Resource()
    for name in ['_links', '_embedded']:
        with pytest.raises(ValueError) as e:
            r.addprop(name, 'foo')
        assert 'reserved' in str(e.value).lower()

def test_can_delete_property():
    name = 'bar'
    r = Resource()
    r.addprop(name, 'foo')
    r.delprop(name)
    assert name not in r.document

def test_del_reserved_properties_raise_error():
    r = Resource()
    for name in ['_links', '_embedded']:
        with pytest.raises(ValueError) as e:
            r.delprop(name)
        assert 'reserved' in str(e.value).lower()

def test_can_embed_other_doc():
    r1 = Resource()
    r2 = Resource()
    r2.addlink('abc', 'def')
    r2.addprop('foo', 'bar')
    r1.addembedded('r2', r2.document)
    assert r1.document['_embedded']['r2'][0] is r2.document

def test_can_autoembed_doc_from_other_resource():
    r1 = Resource()
    r2 = Resource()
    r2.addlink('abc', 'def')
    r2.addprop('foo', 'bar')
    r1.addembedded('r2', r2)
    assert r1.document['_embedded']['r2'][0] is r2.document

def test_can_return_embedded_document():
    r1 = Resource()
    r2 = Resource()
    r2.addlink('abc', 'def')
    r2.addprop('foo', 'bar')
    r1.addembedded('r2', r2)
    assert r1.getembedded('r2')[0] is r2.document

def test_can_delete_embedded():
    r1 = Resource()
    r2 = Resource()
    r2.addlink('abc', 'def')
    r2.addprop('foo', 'bar')
    r1.addembedded('r2', r2)
    r1.delembedded('r2')
    assert 'r2' not in r1.document['_embedded']

def test_can_access_embedded_object_through_property():
    r1 = Resource()
    r2 = Resource()
    r2.addlink('abc', 'def')
    r2.addprop('foo', 'bar')
    r1.addembedded('r2', r2)
    r1.delembedded('r2')
    assert r1.embedded is r1.document['_embedded']

