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
    r.link('abc', abc)
    assert r.document['_links']['abc'][0]['href']==abc

def test_link_properly_set_in_document():
    r = Resource()
    abc = 'http://someurl.com/foo/bar'
    r.link('abc', abc)
    assert r.document['_links']['abc'][0]['href']==abc

def test_templated_flag_can_be_set():
    r = Resource()
    href = 'foo+and+bar+{bar}'
    r.link('abc', href, templated=True)
    assert r.document['_links']['abc'][0]['templated'] is True

def test_templated_flag_is_either_True_or_False():
    r = Resource()
    href = 'foo+and+bar+{bar}'
    r.link('abc', href, templated='whatever')
    assert r.document['_links']['abc'][0]['templated'] is False

def test_can_set_name():
    r = Resource()
    href = 'foo+and+bar+{bar}'
    name = 'next'
    r.link('nav', href, name=name)
    assert r.document['_links']['nav'][0]['name']==name

def test_can_set_media_type():
    r = Resource()
    href = 'foo+and+bar+{bar}'
    mt = 'fubar'
    r.link('abc', href, media_type=mt)
    assert r.document['_links']['abc'][0]['type']==mt

def test_can_set_hreflang():
    r = Resource()
    href = 'foo+and+bar+{bar}'
    lang = 'fr'
    r.link('abc', href, hreflang=lang)
    assert r.document['_links']['abc'][0]['hreflang']==lang

def test_can_set_title():
    r = Resource()
    href = 'foo+and+bar+{bar}'
    title = 'this title'
    r.link('abc', href, title=title)
    assert r.document['_links']['abc'][0]['title']==title

def test_can_set_profile():
    r = Resource()
    href = 'foo+and+bar+{bar}'
    profile = 'some profile'
    r.link('abc', href, profile=profile)
    assert r.document['_links']['abc'][0]['profile']==profile

def test_can_set_deprecation():
    r = Resource()
    href = 'foo+and+bar+{bar}'
    deprecation = 'deprecated in 2020'
    r.link('abc', href, deprecation=deprecation)
    assert r.document['_links']['abc'][0]['deprecation']==deprecation

def test_l_aliases_to_link():
    r = Resource()
    href = 'foo and bar'
    r.l('abc', href) 
    assert r.document['_links']['abc'][0]['href']==href

def test_can_chain_link_methods():
    r = Resource()
    r.l('first', 'foo').l('second', 'bar')
    links = r.document['_links']
    assert links['first'][0]['href']=='foo' and links['second'][0]['href']=='bar'

def test_returns_link_if_no_href():
    r = Resource()
    r.l('first', 'foo').l('second', 'bar')
    assert r.link('first')[0]['href']=='foo' and r.link('second')[0]['href']=='bar'

def test_can_add_curie():
    r = Resource()
    r.curie('first', 'foo/{ref}')
    curies = r.document['_links']['curies']
    assert curies[0]['name']=='first'
    assert curies[0]['href']=='foo/{ref}'

def test_curie_without_ref_raises_exc():
    r = Resource()
    with pytest.raises(ValueError) as e:
        r.curie('first', 'foo')
    assert str(e.value)=="Missing '{ref}' placeholder in uri string."

def test_strict_param_set_to_False_suppresses_curie_missing_ref_exception():
    r = Resource()
    r.curie('first', 'foo', strict=False)
    curies = r.document['_links']['curies']
    assert curies[0]['name']=='first'
    assert curies[0]['href']=='foo'

def test_curie_templated_flag_set(): 
    r = Resource()
    r.curie('first', 'foo',strict=False)
    curies = r.document['_links']['curies']
    assert curies[0]['templated'] is True

def test_c_aliases_to_curie():
    r = Resource()
    r.c('first', 'foo', strict=False)
    curies = r.document['_links']['curies']
    assert curies[0]['name']=='first'
    assert curies[0]['href']=='foo'

def test_can_retrieve_curie_by_name():
    r = Resource()
    r.c('first', 'foo', strict=False)
    assert r.c('first')['name']=='first'
    assert r.c('first')['href']=='foo'

def test_curie_chainable(): 
    r = Resource()
    r.c('first', 'foo', strict=False).c('second', 'bar/{ref}')
    assert r.c('first')['href']=='foo' and r.c('second')['href']=='bar/{ref}'

def test_Resource_can_proxy_to_URIQuote():
    r = Resource()
    urq = r.quote('first and last')
    assert urq.uri=='first%20and%20last'

