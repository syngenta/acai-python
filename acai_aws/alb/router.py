from acai_aws.apigateway.router import Router as ApigatewayRouter
from acai_aws.alb.request import Request
from acai_aws.alb.response import Response


class Router(ApigatewayRouter):
    request_class = Request
    response_class = Response
