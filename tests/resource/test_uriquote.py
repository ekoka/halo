from halo.resource import URIQuote

def test_can_quote_uri():
    urq = URIQuote()
    unquoted = 'foo and bar/{baz}'
    quoted = 'foo%20and%20bar/%7bbaz%7d'
    assert urq.q(unquoted).uri==quoted

def test_can_unquote_uri():
    urq = URIQuote()
    unquoted = 'foo and bar/{baz}'
    quoted = 'foo%20and%20bar/%7bbaz%7d'
    assert urq.uq(quoted).uri==unquoted

def test_uri_normalized_to_lowercase():
    quoted = 'FU/baR/baz%2A'
    unquoted = 'FU/baR/baz*'
    assert URIQuote(quoted).uri==quoted.lower()
    assert URIQuote().uq(quoted).uri==unquoted.lower()

def test_can_quote_space_to_plus():
    urq = URIQuote()
    unquoted = 'foo and bar'
    quoted = 'foo+and+bar'
    assert urq.qp(unquoted).uri==quoted

def test_can_unquote_plus_to_space():
    urq = URIQuote()
    quoted = 'foo+and+bar'
    unquoted = 'foo and bar'
    assert urq.uqp(quoted).uri==unquoted

def test_URIQuote_chainable():
    urq = URIQuote()
    result = 'foo/bar and baz%20'
    assert urq.q('foo').q('/bar').uq('%20').q('and').uq('%20').q('baz ').uri==result

def test_URIQuote_uri_string_not_mutated():
    urq1 = URIQuote('abc')
    urq2 = urq1.q('/def')
    urq3 = urq2.q('/ghi')
    urq4 = urq1.q('/jkl')
    assert urq1.uri=='abc'
    assert urq2.uri=='abc/def'
    assert urq3.uri=='abc/def/ghi'
    assert urq4.uri=='abc/jkl'

