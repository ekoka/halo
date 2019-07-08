from urllib import parse 

_undef = object()

class URIQuote:
    def __init__(self, uri=''):
        self.uri = uri.lower()

    def quote(self, uri):
        return URIQuote(self.uri + parse.quote(uri))

    def unquote(self, uri):
        return URIQuote(self.uri + parse.unquote(uri))

    def unquote_plus(self, uri):
        return URIQuote(self.uri + parse.unquote_plus(uri))

    def quote_plus(self, uri):
        return URIQuote(self.uri + parse.quote_plus(uri))

    q=quote
    uq=unquote
    uqp=unquote_plus
    qp=quote_plus


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
        if attr in URIQuote.__dict__:
            return getattr(URIQuote(), attr) 
        raise AttributeError(
            "'Resource' object has no attribute '{}'".format(attr))

    # link
    def link(self, link, uri='', templated=False, media_type=None, **kw):
        links = self.document.setdefault('_links', {}).setdefault(link, [])

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
            raise KeyError("No {} link in document".format(link))

        if name is None:
            return linkitems
        for l in linkitems:
            if l.get('name')==name:
                return l
        raise KeyError("No link item with name '{}'".format(name))


    #TODO: remove a link
    #TODO: replace a link
    #TODO: remove a curie

    def curie(self, name, uri='', **kw):
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
        curies = self.getlink('curies')
        for c in curies:
            if c['name']==name:
                return c
        raise KeyError("No curie with name '{}'".format(name))

    def prop(self, name, value=_undef):
        if name in ['_links', '_embedded']:
            raise ValueError("'{}' is a HAL reserved name".format(name))

        if value is _undef:
            try:
                return self.document[name]
            except KeyError:
                raise KeyError("Property '{}' not set on document".format(name))
        self.document[name] = value
        return self

    def delprop(self, name):
        if name in ['_links', '_embedded']:
            raise ValueError("'{}' is a HAL reserved name".format(name))
        try:
            self.document.pop(name)
        except KeyError:
            pass
        return self

    def embed(self, name, document=_undef):
        res = self.document.setdefault('_embedded', {}).setdefault(name, [])
        if document is _undef:
            try:
                return self.document['_embedded'][name]
            except KeyError:
                raise KeyError(
                    "Embedded resource '{}' not set on document".format(name))
        if isinstance(document, Resource):
            document = document.document
        res.append(document)
        return self

    def delembed(self, name):
        try:
            self.document['_embedded'].pop(name)
        except KeyError:
            pass
        return self




    # aliases
    l = link
    c = curie
    getl = getlink
    getc = getcurie

