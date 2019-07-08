import pytest
from halo.resource import Resource

def test_can_create_resource_without_document():
    r = Resource()

def test_resource_given_default_document():
    r = Resource()
    assert r.document=={}

def test_link_set_as_tuple_in_document():
    r = Resource()
    abc = 'http://someurl.com/foo/bar'
    r.addlink('abc', abc)
    assert r.document['_links']['abc'][0]['href']==abc

def test_link_properly_set_in_document():
    r = Resource()
    abc = 'http://someurl.com/foo/bar'
    r.addlink('abc', abc)
    assert r.document['_links']['abc'][0]['href']==abc

def test_can_access_links_object_through_property():
    r = Resource()
    abc = 'http://someurl.com/foo/bar'
    r.addlink('abc', abc)
    assert r.links is r.document['_links']

def test_templated_flag_can_be_set():
    r = Resource()
    href = 'foo+and+bar+{bar}'
    r.addlink('abc', href, templated=True)
    assert r.document['_links']['abc'][0]['templated'] is True

def test_templated_flag_is_either_True_or_False():
    r = Resource()
    href = 'foo+and+bar+{bar}'
    r.addlink('abc', href, templated='whatever')
    assert r.document['_links']['abc'][0]['templated'] is False

def test_can_set_name():
    r = Resource()
    href = 'foo+and+bar+{bar}'
    name = 'next'
    r.addlink('nav', href, name=name)
    assert r.document['_links']['nav'][0]['name']==name

def test_can_set_media_type():
    r = Resource()
    href = 'foo+and+bar+{bar}'
    mt = 'fubar'
    r.addlink('abc', href, media_type=mt)
    assert r.document['_links']['abc'][0]['type']==mt

def test_can_set_hreflang():
    r = Resource()
    href = 'foo+and+bar+{bar}'
    lang = 'fr'
    r.addlink('abc', href, hreflang=lang)
    assert r.document['_links']['abc'][0]['hreflang']==lang

def test_can_set_title():
    r = Resource()
    href = 'foo+and+bar+{bar}'
    title = 'this title'
    r.addlink('abc', href, title=title)
    assert r.document['_links']['abc'][0]['title']==title

def test_can_set_profile():
    r = Resource()
    href = 'foo+and+bar+{bar}'
    profile = 'some profile'
    r.addlink('abc', href, profile=profile)
    assert r.document['_links']['abc'][0]['profile']==profile

def test_can_set_deprecation():
    r = Resource()
    href = 'foo+and+bar+{bar}'
    deprecation = 'deprecated in 2020'
    r.addlink('abc', href, deprecation=deprecation)
    assert r.document['_links']['abc'][0]['deprecation']==deprecation

def test_al_aliases_to_link():
    r = Resource()
    href = 'foo and bar'
    r.al('abc', href) 
    assert r.document['_links']['abc'][0]['href']==href

def test_can_chain_link_methods():
    r = Resource()
    r.al('first', 'foo').al('second', 'bar')
    links = r.document['_links']
    assert links['first'][0]['href']=='foo' and links['second'][0]['href']=='bar'

def test_can_return_link():
    r = Resource()
    r.al('first', 'foo').al('second', 'bar')
    assert r.getlink('first')[0]['href']=='foo' 
    assert r.getlink('second')[0]['href']=='bar'

def test_can_filter_returned_link_by_name():
    r = Resource()
    r.al('nav', '/page/1', name='first').al('nav', '/page/2', name='next')
    assert r.getlink('nav', name='first')['href']=='/page/1' 
    assert r.getlink('nav', name='next')['href']=='/page/2'

def test_raise_error_if_link_not_found():
    r = Resource()
    r.al('nav', '/page/1', name='first').al('nav', '/page/2', name='next')
    with pytest.raises(KeyError) as e:
        r.getlink('foo')
    assert 'not found' in str(e.value).lower()

def test_raise_error_if_name_not_found_in_existing_link():
    r = Resource()
    r.al('nav', '/page/1', name='first').al('nav', '/page/2', name='next')
    with pytest.raises(KeyError) as e:
        r.getlink('nav', name='last')
    assert 'not found' in str(e.value).lower()

def test_can_delete_link_collection():
    r = Resource()
    r.al('nav', '/page/1', name='first').al('nav', '/page/2', name='next')
    r.dellink('nav')
    assert 'nav' not in r.document['_links']

def test_can_delete_named_item_in_link_collection():
    r = Resource()
    r.al('nav', '/page/1', name='first').al('nav', '/page/2', name='next')
    r.dellink('nav', name='first')
    assert r.document['_links']['nav'][0]['name']=='next'

def test_can_add_curie():
    r = Resource()
    r.addcurie('first', 'foo/{ref}')
    curies = r.document['_links']['curies']
    assert curies[0]['name']=='first'
    assert curies[0]['href']=='foo/{ref}'

def test_curie_without_ref_raises_exc():
    r = Resource()
    with pytest.raises(ValueError) as e:
        r.ac('first', 'foo')
    assert str(e.value)=="Missing '{ref}' placeholder in uri string."

def test_strict_param_set_to_False_suppresses_curie_missing_ref_exception():
    r = Resource()
    r.ac('first', 'foo', strict=False)
    curies = r.document['_links']['curies']
    assert curies[0]['name']=='first'
    assert curies[0]['href']=='foo'

def test_curie_templated_flag_set(): 
    r = Resource()
    r.ac('first', 'foo',strict=False)
    curies = r.document['_links']['curies']
    assert curies[0]['templated'] is True

def test_c_aliases_to_curie():
    r = Resource()
    r.ac('first', 'foo', strict=False)
    curies = r.document['_links']['curies']
    assert curies[0]['name']=='first'
    assert curies[0]['href']=='foo'

def test_can_retrieve_curie_by_name():
    r = Resource()
    r.ac('first', 'foo', strict=False)
    assert r.gc('first')['name']=='first'
    assert r.gc('first')['href']=='foo'

def test_curie_chainable(): 
    r = Resource()
    r.ac('first', 'foo', strict=False).ac('second', 'bar/{ref}')
    assert r.gc('first')['href']=='foo' 
    assert r.gc('second')['href']=='bar/{ref}'

def test_can_access_curies_object_through_property():
    r = Resource()
    r.ac('first', 'foo', strict=False).ac('second', 'bar/{ref}')
    r.curies is r.document['_links']['curies']

def test_can_delete_curie():
    r = Resource()
    r.ac('first', 'foo', strict=False).ac('second', 'bar/{ref}')
    r.delcurie('first')
    with pytest.raises(KeyError) as e:
        r.gc('first')
    assert 'not found' in str(e.value).lower()
 
def test_can_chain_curie_deletion():
    r = Resource()
    r.ac('first', 'foo', strict=False).ac('second', 'bar/{ref}')
    assert len(r.dc('first').dc('second').curies) == 0

def test_Resource_can_proxy_to_URIQuote():
    r = Resource()
    urq = r.quote('first and last')
    assert urq.uri=='first%20and%20last'

