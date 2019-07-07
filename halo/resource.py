from urllib import parse 

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
    def link(self, name, uri=None, templated=False, **kw):
        links = self.document.setdefault('_links', {}).setdefault(name, [])

        if uri is None:
            return links

        link = {'href':uri.lower()}
        if templated:
            link['templated'] = templated
        links.append(link)
        return self

    def curie(self, name, uri=None, **kw):
        if kw.get('strict') is None:
            kw['strict'] = True
        curies = self.link('curies')
        try:
            curie = [c for c in curies if c['name']==name][0]
        except IndexError:
            curie = {'name': name, 'templated':True}
            curies.append(curie)
        
        if uri is None:
            return curie
        href = uri.lower()
        if '{ref}' not in href and kw.get('strict') is True:
            raise ValueError("Missing '{ref}' placeholder in uri string.")
        curie['href'] = uri.lower()

        return self


    # aliases
    l = link
    c = curie

