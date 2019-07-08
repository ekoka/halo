# HALO (Hypertext Application Language Output)

HAL ([1](http://stateless.co/hal_specification.html), [2](https://tools.ietf.org/html/draft-kelly-json-hal-08), [3](https://en.wikipedia.org/wiki/Hypertext_Application_Language)) is a simple format to organize hypertext resources in an API. It improves navigation and discoverability of the API by client applications that understand the format.

HALO is a small Python utility that helps you serve your resources using the HAL specification. It currently only returns resources in JSON.

A corresponding tool is available to read formatted HAL documents called HALI (HAL Input) written in ES6 JavaScript. It can be helpful when consuming HAL formatted resources (e.g. from an API). 

# Creating a HAL Resource

Simply creating a `halo.Resource` object creates an empty resource.

    ```python
    import halo

    resource = halo.Resource()
    ```
You can access the raw document from the `Resource.document` property.

    ```
    resource.document
    # {}
    ```

Alternatively you can pass an existing document to the `Resource` constructor.

    ```python
    import halo

    document = {
        '_links': {
            'self': '/products/73'
        },
        name: 'Blue pen'
    }
    resource = halo.Resource(document)
    ```

# Working with links

HALO allows you to do a number of common operations on your document's `_links` object.

### Adding a link

    ```python
    resource.addlink('first', 'https://example.org/pages/1')

    # or using a short alias

    resource.al('next', 'https://example.org/pages/2')
    ```
Most setter and deleter methods return the same `Resource` instance that invokes them. You can take advantage of this to chain those calls. For example, when adding links:

    ```python
    r = halo.Resource()
    r.al(
        'users', 'https://example.org/users').al(
        'products', 'https://example.org/products/73').al(
        'products', 'https://example.org/products/922').al(
        'categories', 'https://example.org/categories')
    ```

If you were to look at the document you'd see something like this

    ```python
    print(r.document)
    ```

    {
        '_links': {
            'users': [
                {'href': 'https://example.org/users'},
            ],
            'products': [
                {'href': 'https://example.org/products/73'},
                {'href': 'https://example.org/products/922'}
            ],
            'categories': [
                {'href': 'https://example.org/categories'}
            ]
        }
    }

Note that normally a relation (e.g. 'users', 'products', 'categories', etc) points to a single link. However, HAL also allows for the possibility of one relation pointing to a collection of links. To provide some consistency when handling links in client applications, HALO always represent them as a collection, whether a link should be considered a single item or otherwise. To differentiate between links that are part of an actual collection, it is recommended to provide them with an additional `name` attribute, that will be used to segregate them, as demonstrated below.

    ```python
    books = halo.Resource()
    books.al(
        'nav', '/books/1', name='first').al(
        'nav', '/books/2', name='next').al(
        'nav', '/books/87', name='last')
    print(books.document)
    ```
    {
        '_links': {
            'nav': [
                {
                    'name': 'first'
                    'href': '/books/1'
                },
                {
                    'name': 'next'
                    'href': '/books/2'
                },
                {
                    'name': 'last'
                    'href': '/books/87'
                }
            ]
        }
    }

Details on how to treat links in client applications are left to each API's specification (and to client implementations). My own APIs are standardized around the convention that if the first item of a link collection is missing the `name` attribute, that collection should be treated as a single item collection, else if `name` is present, the collection should be considered to contain multiple links. Short of such a convention, I'd have to specify how links should be treated.

### Retrieving links

To retrieve a previously set link, call the `getlink()` method or its `gl()` alias, passing the relation as first parameter.

    ```
    nav = r.gl('nav')
    print(nav)
    ```
    [
        {
            'name': 'first'
            'href': '/books/1'
        },
        {
            'name': 'next'
            'href': '/books/2'
        },
        {
            'name': 'last'
            'href': '/books/87'
        }
    ]
   
To return only one of the links in a collection based on its name, do the same but in addition to the relation, specify the `name` of the link you want:

    ```
    last = r.gl('nav', name='last')
    print(last)
    ```
    {
        'name': 'last'
        'href': '/books/87'
    }

You can also access a document's `_links` object with the `Resource.links` property, if you need to directly manipulate it.

    ```
    r.document['_links'] is r.links 
    #True
    ```

Trying to access a link that is not in the document throws a `KeyError`.

    ```
    r.gl('profile')
    KeyError: Link 'profile' not found in document
    ```

### Deleting links

You can delete links with the `dellink(link)` method or its alias `dl(link)`. 

    r.dl('nav')

The method is chainable, allowing you to  

# TODO: URL Encoding and decoding

    

