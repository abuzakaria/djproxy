"""HTTP Reverse Proxy class based generic view."""


from pyramid.response import Response
from requests import request

from .headers import HeaderDict
from .proxy_middleware import MiddlewareSet
from .request import DownstreamRequest

from urllib.parse import urlparse

class HttpProxy(object):
    """Reverse HTTP Proxy class-based generic view."""

    proxy_url = None
    ignored_headers = [
        'Content-Length', 'Content-Encoding', 'Keep-Alive', 'Connection',
        'Transfer-Encoding', 'Host', 'Expect', 'Upgrade']
    proxy_middleware = [
        'djproxy.proxy_middleware.AddXFF',
        'djproxy.proxy_middleware.AddXFH',
        'djproxy.proxy_middleware.AddXFP',
        'djproxy.proxy_middleware.ProxyPassReverse'
    ]
    pass_query_string = True
    verify_ssl = True
    cert = None
    timeout = None

    def __init__(self, url):
        """Return URL to the resource to proxy."""
        self.proxy_url = url
        self.hostname = urlparse(url).hostname


    def _verify_config(self):
        assert self.proxy_url, 'base_url must be set to generate a proxy url'

        iter(self.ignored_headers)
        iter(self.proxy_middleware)

    def dispatch(self, request, *args, **kwargs):
        """Dispatch all HTTP methods to the proxy."""
        self.request = DownstreamRequest(request)
        self.args = args
        self.kwargs = kwargs

        self._verify_config()

        self.middleware = MiddlewareSet(self.proxy_middleware)

        return self.proxy()


    def proxy(self):
        """Retrieve the upstream content and build an HttpResponse."""
        headers = self.request.headers
        headers.environ['HTTP_HOST'] = self.hostname
        qs = self.request.query_string if self.pass_query_string else ''

        request_kwargs = self.middleware.process_request(
            self, self.request, method=self.request.method, url=self.proxy_url,
            headers=headers, data=self.request.body, params=qs,
            allow_redirects=False, verify=self.verify_ssl, cert=self.cert,
            timeout=self.timeout)

        result = request(**request_kwargs)

        response = Response(result.content, status=result.status_code)

        # Attach forwardable headers to response
        forwardable_headers = HeaderDict(result.headers).filter(
            self.ignored_headers)
        response._headerlist__set(forwardable_headers)
        return self.middleware.process_response(
            self, self.request, result, response)
