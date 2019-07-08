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
    > {
    .     '_links': {
    .         'users': [
    .             {'href': 'https://example.org/users'},
    .         ],
    .         'products': [
    .             {'href': 'https://example.org/products/73'},
    .             {'href': 'https://example.org/products/922'}
    .         ],
    .         'categories': [
    .             {'href': 'https://example.org/categories'}
    .         ]
    .     }
    . }
    ```

Note that normally a relation (e.g. 'users', 'products', 'categories', etc) points to a single link. However, HAL also allows for the possibility of one relation pointing to a collection of links. To provide some consistency when handling links in client applications, HALO always represent them as a collection, whether a link should be considered a single item or otherwise. To differentiate between links that are part of an actual collection, it is recommended to provide them with an additional `name` attribute, that will be used to segregate them, as demonstrated below.

    ```python
    books = halo.Resource()
    books.al(
        'nav', '/books/1', name='first').al(
        'nav', '/books/2', name='next').al(
        'nav', '/books/87', name='last')
    print(books.document)
    > {
    .     '_links': {
    .         'nav': [
    .             {
    .                 'name': 'first'
    .                 'href': '/books/1'
    .             },
    .             {
    .                 'name': 'next'
    .                 'href': '/books/2'
    .             },
    .             {
    .                 'name': 'last'
    .                 'href': '/books/87'
    .             }
    .         ]
    .     }
    . }
    ```

Details on how to treat links in client applications are left to each API's specification (and to client implementations). My own APIs are standardized around the convention that if the first item of a link collection is missing the `name` attribute, that collection should be treated as a single item collection, else if `name` is present, the collection should be considered to contain multiple links. Short of such a convention, I'd have to specify how links should be treated.

### Retrieving links

To retrieve a previously set link, call the `getlink(rel)` method or its `gl(rel)` alias, passing the relation as first parameter.

    ```
    nav = r.gl('nav')
    print(nav)
    > [
    .     {
    .         'name': 'first'
    .         'href': '/books/1'
    .     },
    .     {
    .         'name': 'next'
    .         'href': '/books/2'
    .     },
    .     {
    .         'name': 'last'
    .         'href': '/books/87'
    .     }
    . ]
    ```
   
To return only one of the links in a collection based on its `name` attribute, do the same as the above but in addition to the relation, specify the `name` of the link you want:

    ```
    last = r.gl('nav', name='last')
    print(last)
    > {
    .     'name': 'last'
    .     'href': '/books/87'
    . }
    ```

You can also access a document's `_links` object with the `Resource.links` property, if you need to directly manipulate it.

    ```
    r.document['_links'] is r.links 
    > True
    ```

Trying to access a link that is not in the document throws a `KeyError`.

    ```
    r.gl('profile')
    KeyError: Link 'profile' not found in document
    ```

### Deleting links

You can delete links with the `dellink(rel)` method or its alias `dl(rel)`. 

    r.dl('nav')

To remove only a specific link from the collection, specify its `name` attribute.

    r.dl('nav', 'next')

The method is chainable, allowing you to continue operating on the `Resource` instance.

### URI encoding and decoding

HAL does not enforce a particular way to handle URIs. Whether you should encode them prior to adding them to resources, or leave them decoded is up to your implementation. Nonetheless, there needs to be a clear approach that is communicated to client applications, so as not to create confusion.

HALO takes the stance of providing API developers with the flexibility afforded by HAL and does not enforce one approach or another either. Instead it provides a small set of utilities that allow to build your URIs while encoding and decoding the parts that you want.

You can do a number of encoding/decoding operations with a `halo.URIEncode` object.

    u = halo.URIEncode('http://example.com/')
    u = u.encode('foo and bar')
    print(u.uri)
    > http://example.com/foo%20and%20bar

The example above can be a bit deceptive. It's important to understand how `URIEncode` works, so let us first go through a few more examples to get a sense of what's going on

Create an instance of `URIEncode` with a base URI string.

    q1 = halo.URIEncode('http://example.com/') 
    print(q1.uri)
    > http://example.com/

Upon asking for an additional string to be encoded, a new instance of `URIEncode` is returned

    q2 = q1.encode('foo and bar') 
    q1 is q2
    > False

The URI string in the first instance has not changed, though

    print(q1.uri) 
    > http://example.com/

and the second instance contains the string from the first instance, plus the encoded version of the second string, as per requested

    print(q2.uri)
    > http://example.com/foo%20and%20bar

You can thus chain the construction of your URIs to URL encode or decode as you see fit

    q3 = q2.decode('/%2frel%2g').encode('/:name').plain('/section/{s}')
    print(q3.uri)
    > http://example.com/foo%20and%20bar/{rel}/%a3name/section/{s}

    q4 = q3.plain('/baz/{id}')
    print(q4.uri)
    > http://example.com/foo%20and%20bar/{rel}/baz/{id}

For convenience, some methods from `Resource` proxy to `URIEncode`'s methods. There are also a number of shorter aliases. In application code this is how you would likely use it

    
    prod_templ = r.enc('http://api.example.com/v1/products/').pln('{product_id}')

    r.addlink('product', prod_templ.uri, templated=True)

    print(r.links)
    > {
    .     '_links': {
    .         'product': [
    .             {
    .                 'href': 'http%3a//api.example.com/v1/products/{product_id}',
    .                 'templated': True,
    .             }
    .         ]
    .     }
    . }


The `URIEncode` class gives you great flexibility in how to structure your resource's URLs, but as you know, with great power comes great responsibility. It's generally not a good idea to mix encoded characters with non-encoded ones. So avoid doing that unless it's absolutely necessary, as it is in the case of URL templates, which use curly braces to delimit the placeholder. Even in such cases you should thoroughly document your URI templates to clarify the steps to take prior to processing the template to generate a URL (e.g. should the template be entirely url-decoded first, or is it served with the placeholder already in its curly brace form, ready to be replaced by a key).
