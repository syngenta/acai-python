from openapi_core.datatypes import RequestParameters

class AcaiOpenAPIRequest:

    def __init__(self, request):
        self.request = request

        self.parameters = RequestParameters(
            query=request.query_params,
            header=request.headers,
            cookie=request.cookies
        )

    @property
    def host_url(self):
        return self.request.url

    @property
    def path(self):
        return self.request.path

    @property
    def method(self):
        return self.request.method

    @property
    def body(self):
        return self.request.raw

    @property
    def mimetype(self):
        if self.request.headers.get('Content-Type'):
            return self.request.headers['Content-Type'].partition(';')[0]
        return ''
