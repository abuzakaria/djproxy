djproxy
=======
djproxy is a class-based generic view reverse HTTP proxy for Django. Modified in this branch for
pyramid.

Why?
----

If an application depends on a proxy (to get around Same Origin Policy
issues in JavaScript, perhaps), djproxy can be used to provide that
functionality in a web server agnostic way. This allows developers to
keep local development environments for proxy dependent applications
fully functional without needing to run anything other than the pyramid
development server.

djproxy is also suitable for use in production environments and has been
proven to be performant in large scale deployments. However, a web
server's proxy capabilities will be *more* performant in many cases. If
one needs to use this in production, it should be fine as long as
upstream responses aren't large. Performance can be further increased by
aggressively caching upstream responses.

Installation
------------

::

    pip install djproxy



Usage
-----

Start by defining a new proxy:

.. code:: python

    @view_config(route_name='proxy', renderer='proxy_iframe.jinja2')
    def proxy(request):
        url = 'http://bugs.python.org'
        proxy_view = HttpProxy(url)
        response = proxy_view.dispatch(request)
        return {
            'content': response.text
        }


Add a route:

.. code:: python

    ROUTES = [
        ('homepage', ''),
        ('proxy', '/proxy'),
    ]


In proxy_iframe.jinja2 :

::

    {{ content|safe }}

