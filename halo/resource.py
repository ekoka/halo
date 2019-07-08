from urllib import parse 

_undef = object()

class URIEncode:
    def __init__(self, uri=''):
        self.uri = uri.lower()

    def plain(self, uri):
        return URIEncode(self.uri + uri)

    def encode(self, uri):
        return URIEncode(self.uri + parse.quote(uri))

    def decode(self, uri):
        return URIEncode(self.uri + parse.unquote(uri))

    def decode_plus(self, uri):
        return URIEncode(self.uri + parse.unquote_plus(uri))

    def encode_plus(self, uri):
        return URIEncode(self.uri + parse.quote_plus(uri))

    pln=plain
    enc=encode
    dec=decode
    decp=decode_plus
    encp=encode_plus


class Resource:

    media_type = 'application/hal+json'

    def __init__(self, hal_or_document=None):
        if hal_or_document is None:
            document = {}
        else:
            try:
                document = hal_or_document.document
            except AttributeError as e:
                document = hal_or_document
        self.document = document

    def __getattr__(self, attr):
        if attr in URIEncode.__dict__:
            return getattr(URIEncode(), attr) 
        raise AttributeError(
            "'Resource' object has no attribute '{}'".format(attr))

    @property
    def links(self):
        return self.document.setdefault('_links', {})

    @property
    def curies(self):
        return self.links.setdefault('curies', [])

    @property
    def embedded(self):
        return self.document.setdefault('_embedded', {})

    # link
    def addlink(self, link, uri='', templated=False, media_type=None, **kw):
        links = self.links.setdefault(link, [])
        linkitem = {'href':uri.lower()}
        if templated is not None: 
            linkitem['templated'] = (templated is True) or False 
        if media_type is not None:
            linkitem['type'] = media_type
        for k in ['name', 'hreflang', 'title', 'profile', 'deprecation']:
            if kw.get(k) is not None:
                linkitem[k] = kw[k]
        links.append(linkitem)
        return self

    def getlink(self, link, name=None):
        try:
            linkitems = self.document['_links'][link]
        except KeyError:
            raise KeyError("Link '{}' not found in document".format(link))
        if name is None:
            return linkitems
        for l in linkitems:
            if l.get('name')==name:
                return l
        raise KeyError("Link item with name '{}' not found".format(name))

    def dellink(self, link, name=None):
        links = self.document.get('_links', {})
        if name is None:
            links.pop(link, None)
        elif links.get(link):
            links[link] = [l for l in links[link] if l.get('name')!=name]
        return self

    def addcurie(self, name, uri='', **kw):
        if kw.get('strict') is None:
            kw['strict'] = True
        curies = self.document.setdefault('_links', {}).setdefault('curies', [])
        try:
            curie = [c for c in curies if c['name']==name][0]
        except IndexError:
            curie = {'name': name, 'templated':True}
            curies.append(curie)
        href = uri.lower()
        if '{ref}' not in href and kw.get('strict') is True:
            raise ValueError("Missing '{ref}' placeholder in uri string.")
        curie['href'] = uri.lower()
        return self

    def getcurie(self, name):
        try:
            curies = self.document['_links']['curies']
            for c in curies:
                if c['name']==name:
                    return c
        except KeyError:
            pass
        raise KeyError("Curie with name '{}' not found".format(name))

    def delcurie(self, name):
        try:
            links = self.document['_links']
            links['curies'] = [c for c in links['curies'] if c['name']!=name]
        except KeyError:
            pass
        return self

    def addprop(self, name, value=None):
        if name in ['_links', '_embedded']:
            raise ValueError("'{}' is a HAL reserved name".format(name))
        self.document[name] = value
        return self

    def getprop(self, name):
        try:
            return self.document[name]
        except KeyError:
            raise KeyError("Property '{}' not found on document".format(name))

    def delprop(self, name):
        if name in ['_links', '_embedded']:
            raise ValueError("'{}' is a HAL reserved name".format(name))
        try:
            self.document.pop(name)
        except KeyError:
            pass
        return self

    def addembedded(self, name, document):
        res = self.document.setdefault('_embedded', {}).setdefault(name, [])
        if isinstance(document, Resource):
            document = document.document
        res.append(document)
        return self

    def getembedded(self, name):
        try:
            return self.document['_embedded'][name]
        except KeyError:
            raise KeyError(
                "Embedded resource '{}' not found on document".format(name))

    def delembedded(self, name):
        try:
            self.document['_embedded'].pop(name)
        except KeyError:
            pass
        return self

    # aliases
    al = addlink
    ac = addcurie
    ae = addembedded
    ap = addprop
    gl = getlink
    gc = getcurie
    ge = getembedded
    gp = getprop
    dl = dellink
    dc = delcurie
    de = delembedded
    dp = delprop


