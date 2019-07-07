from urllib import parse 

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

    def _process_link(self, uri, **kw):
        # unless `unquote` is explicitly set to False unquote all urls.
        if kw.get('unquote') is not False:
            kw['unquote'] = True

        # unquote_plus supersedes unquote
        for q in ['unquote_plus', 'unquote']:
            if kw.get(q):
                uri = getattr(parse, q)(uri)
                break

        for q in ['quote_plus', 'quote']:
            if kw.get(q):
                uri = getattr(parse, q)(uri)
                break
        return uri.lower()

    # link
    def link(self, name, uri=None, templated=False, **kw):
        links = self.document.setdefault('_links', {}).setdefault(name, [])

        if uri is None:
            return links

        link = {'href':self._process_link(uri, **kw)}
        if templated:
            link['templated'] = templated
        links.append(link)
        return self

    def curie(self, name, uri=None, **kw):
        curies = self.link('curies')
        try:
            curie = [c for c in curies if c['name']==name][0]
        except IndexError:
            curie = {'name': name, 'templated':True}
            curies.append(curie)
        
        if uri is None:
            return curie
        href = self._process_link(uri, **kw)
        if '{ref}' not in href and kw.get('strict') is True:
            raise ValueError("Missing '{ref}' placeholder in uri string.")
        curie['href'] = self._process_link(uri, **kw)

        return self



    # aliases
    l = link
    c = curie

