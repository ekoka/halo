from urllib import parse 

class Resource:

    def __init__(self, hal_or_document=None):
        if hal_or_document is None:
            document = {}
        else:
            try:
                document = hal_or_document.document
            except AttributeError as e:
                document = hal_or_document
        self.document = document


    # links
    def link(self, name, uri, templated=False, **kw):# quote=False, unquote=False):
        # unquote_plus  supersedes unquote
        for q in ['unquote_plus', 'unquote']:
            if kw.get(q):
                uri = getattr(parse, q)(uri)
                break

        for q in ['quote_plus', 'quote']:
            if kw.get(q):
                uri = getattr(parse, q)(uri)
                break

        link = {'href':uri.lower()}
        if templated:
            link['templated'] = templated
        links = self.document.setdefault('_links', {})
        links[name] = link
        return self

    # alias l to link
    l = link

