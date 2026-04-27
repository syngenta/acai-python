from acai_aws.apigateway.response import Response as ApigatewayResponse


_STATUS_DESCRIPTIONS = {
    200: 'OK',
    201: 'Created',
    202: 'Accepted',
    204: 'No Content',
    301: 'Moved Permanently',
    302: 'Found',
    304: 'Not Modified',
    400: 'Bad Request',
    401: 'Unauthorized',
    403: 'Forbidden',
    404: 'Not Found',
    405: 'Method Not Allowed',
    408: 'Request Timeout',
    409: 'Conflict',
    422: 'Unprocessable Entity',
    429: 'Too Many Requests',
    500: 'Internal Server Error',
    502: 'Bad Gateway',
    503: 'Service Unavailable',
    504: 'Gateway Timeout',
}


class Response(ApigatewayResponse):

    @property
    def status_description(self):
        return f"{self.code} {_STATUS_DESCRIPTIONS.get(self.code, 'OK')}"

    @property
    def full(self):
        return {**super().full, 'statusDescription': self.status_description}
