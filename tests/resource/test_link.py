from halo.resource import Resource

def test_can_create_resource_without_document():
    r = Resource()

def test_resource_given_default_document():
    r = Resource()
    assert r.document=={}

def test_link_properly_set_in_document():
    r = Resource()
    abc = 'http://someurl.com/foo/bar'
    r.link('abc', abc)
    assert r.document['_links']['abc']['href']==abc

def test_link_lower_cased():
    r = Resource()
    abc = 'FU/baR/baz%2A'
    r.link('abc', abc)
    assert r.document['_links']['abc']['href']==abc.lower()

def test_link_can_be_quoted():
    r = Resource()
    unquoted = 'foo and bar/{baz}'
    quoted = 'foo%20and%20bar/%7bbaz%7d'
    r.link('abc', unquoted, quote=True)
    assert r.document['_links']['abc']['href']==quoted

def test_link_can_be_unquoted():
    r = Resource()
    quoted = 'foo%20and%20bar/%7bbaz%7d'
    unquoted = 'foo and bar/{baz}'
    r.link('abc', quoted, unquote=True)
    assert r.document['_links']['abc']['href']==unquoted

def test_link_can_quote_space_to_plus():
    r = Resource()
    unquoted = 'foo and bar'
    quoted = 'foo+and+bar'
    r.link('abc', unquoted, quote_plus=True)
    assert r.document['_links']['abc']['href']==quoted

def test_link_can_unquote_plus_to_space():
    r = Resource()
    quoted = 'foo+and+bar'
    unquoted = 'foo and bar'
    r.link('abc', quoted, unquote_plus=True)
    assert r.document['_links']['abc']['href']==unquoted

def test_link_can_be_marked_as_templated():
    r = Resource()
    quoted = 'foo+and+bar+{bar}'
    unquoted = 'foo and bar %7bbar%7d'
    r.link('abc', quoted, templated=True)
    assert r.document['_links']['abc']['templated'] is True

def test_unquote_processed_before_quote():
    # unquote, unquote_plus, quote_plus, quote
    r = Resource()
    start = 'foo%20and%20bar%20{bar}'
    end = 'foo%20and%20bar%20%7bbar%7d'
    r.link('abc', start, quote=True, unquote=True) 
    assert r.document['_links']['abc']['href']==end

def test_unquote_plus_supersedes_quote():
    # unquote, unquote_plus, quote_plus, quote
    r = Resource()
    start = 'foo+and+bar'
    end = 'foo and bar'
    r.link('abc', start, unquote=True, unquote_plus=True) 
    assert r.document['_links']['abc']['href']==end

def test_quote_plus_supersedes_quote():
    r = Resource()
    start = 'foo and bar'
    end = 'foo+and+bar'
    r.link('abc', start, quote=True, quote_plus=True) 
    assert r.document['_links']['abc']['href']==end

def test_l_aliases_to_link():
    r = Resource()
    start = 'foo and bar'
    end = 'foo+and+bar'
    r.l('abc', start, quote=True, quote_plus=True) 
    assert r.document['_links']['abc']['href']==end

def test_can_chain_link_methods():
    r = Resource()
    r.l('first', 'foo').l('second', 'bar')
    links = r.document['_links']
    assert links['first']['href']=='foo' and links['second']['href']=='bar'
