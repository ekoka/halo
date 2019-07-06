# HALO (Hypertext Application Language Output)

A Python tool to create resources following the [HAL specification](http://stateless.co/hal_specification.html). HAL is useful to organize and standardize the format of hypertext resources (e.g. REST).

The only returns resources in JSON type (application/hal+json).

A corresponding tool is available to read formatted HAL documents called HALI (HAL Input) written in ES6 JavaScript. It can be helpful when consuming resources from an API. It wraps the document into an object for easier data access and manipulation. 

# URL Encoding and decoding
When a number of characters in the same URL are different in their URL encoded form from their unicode form, it's not a good idea to mix the representations in the same URL string, as that might lead to confusion. Doing so might not be *wrong* per se, but purely from a practical standpoint, HALO treats this sort of mixing as an oversight and tries to reestablish a level consistency. Thus, when processing links and curies it will first decode their URL, so that any eventual encoded character is reverted to its unicode form, then the string is URL encoded again, thus escaping any URL encodable character. 

Take for instance the following URL

    http://example.com/foo%20and%20bar/{rel}

The first colon character is not URL encoded, but '%20' is the representation of a URL encoded space character. Likewise the `rel` placeholder is surrounded by raw '{' and '}' characters.  

HAL would process this URL by first unencoding it, yielding

    http://example.com/foo and bar/{rel}

Then encoding that result and lowercasing the result to give

    http%3a//example.com/foo%20and%20bar/%7brel%7d


[1](https://en.wikipedia.org/wiki/Hypertext_Application_Language)
