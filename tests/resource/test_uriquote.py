from halo.resource import URIEncode

def test_can_encode_uri():
    urq = URIEncode()
    decoded = 'foo and bar/{baz}'
    encoded = 'foo%20and%20bar/%7bbaz%7d'
    assert urq.enc(decoded).uri==encoded

def test_can_accept_plain_strings():
    ur = URIEncode('abc')
    assert ur.plain(': and :').uri =='abc: and :'

def test_can_decode_uri():
    urq = URIEncode()
    decoded = 'foo and bar/{baz}'
    encoded = 'foo%20and%20bar/%7bbaz%7d'
    assert urq.dec(encoded).uri==decoded

def test_uri_normalized_to_lowercase():
    encoded = 'FU/baR/baz%2A'
    decoded = 'FU/baR/baz*'
    assert URIEncode(encoded).uri==encoded.lower()
    assert URIEncode().dec(encoded).uri==decoded.lower()

def test_can_encode_space_to_plus():
    urq = URIEncode()
    decoded = 'foo and bar'
    encoded = 'foo+and+bar'
    assert urq.encp(decoded).uri==encoded

def test_can_decode_plus_to_space():
    urq = URIEncode()
    encoded = 'foo+and+bar'
    decoded = 'foo and bar'
    assert urq.decp(encoded).uri==decoded

def test_URIEncode_chainable():
    urq = URIEncode()
    result = 'foo/bar and baz%20'
    assert urq.enc('foo').enc('/bar').dec('%20').enc('and').dec('%20').enc('baz ').uri==result

def test_URIEncode_uri_string_not_mutated():
    urq1 = URIEncode('abc')
    urq2 = urq1.enc('/def')
    urq3 = urq2.enc('/ghi')
    urq4 = urq1.enc('/jkl')
    assert urq1.uri=='abc'
    assert urq2.uri=='abc/def'
    assert urq3.uri=='abc/def/ghi'
    assert urq4.uri=='abc/jkl'

