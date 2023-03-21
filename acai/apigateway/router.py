from acai.apigateway.exception import ApiException
from acai.apigateway.request import Request
from acai.apigateway.resolver import Resolver
from acai.apigateway.response import Response
from acai.common.validator import Validator


class Router:

    def __init__(self, **kwargs):
        self.__before_all = kwargs.get('before_all')
        self.__after_all = kwargs.get('after_all')
        self.__with_auth = kwargs.get('with_auth')
        self.__on_error = kwargs.get('on_error')
        self.__auto_validate = kwargs.get('auto_validate')
        self.__resolver = Resolver(**kwargs)
        self.__validator = Validator(**kwargs)

    def route(self, event, context):
        request = Request(event, context)
        response = Response()
        try:
            self.__run_route(request, response)
        except ApiException as api_error:
            response.code = api_error.code
            response.set_error(key_path=api_error.key_path, message=api_error.message)
        except Exception as error:
            response.code = 500
            response.set_error(key_path='unknown', message=str(error))
        if response.has_errors:
            self.__handle_error(request, response)
        return response.full

    def __run_route(self, request, response):
        endpoint = self.__resolver.get_endpoint(request)
        if not response.has_errors and self.__before_all and callable(self.__before_all):
            self.__before_all(request, response, endpoint.requirements)
        if not response.has_errors and endpoint.requires_auth and self.__with_auth and callable(self.__with_auth):
            self.__with_auth(request, response, endpoint.requirements)
        if not response.has_errors and self.__auto_validate:
            self.__validator.validate_request_with_openapi(request, response)
        if not response.has_errors and endpoint.has_requirements:
            self.__validator.validate_request(request, response, endpoint.requirements)
        if not response.has_errors:
            endpoint.run(request, response)
        if not response.has_errors and self.__after_all and callable(self.__after_all):
            self.__after_all(request, response, endpoint.requirements)
        return response

    def __handle_error(self, request, response):
        try:
            if self.__on_error and callable(self.__on_error):
                self.__on_error(request, response)
        except Exception as error:
            print(error)
