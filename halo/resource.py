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


    # alias l to link
    l = link