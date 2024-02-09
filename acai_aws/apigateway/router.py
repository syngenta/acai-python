import logging

from acai_aws.apigateway.exception import ApiException, ApiTimeOutException
from acai_aws.apigateway.request import Request
from acai_aws.apigateway.resolver import Resolver
from acai_aws.apigateway.response import Response
from acai_aws.apigateway.config_validator import ConfigValidator
from acai_aws.common.validator import Validator
from acai_aws.common import logger


class Router:

    def __init__(self, **kwargs):
        ConfigValidator.validate(**kwargs)
        self.__before_all = kwargs.get('before_all')
        self.__after_all = kwargs.get('after_all')
        self.__with_auth = kwargs.get('with_auth')
        self.__on_error = kwargs.get('on_error')
        self.__on_timeout = kwargs.get('on_timeout')
        self.__cors = kwargs.get('cors', True)
        self.__timeout = kwargs.get('timeout', None)
        self.__output_error = kwargs.get('output_error', False)
        self.__verbose = kwargs.get('verbose_logging', False)
        self.__auto_validate = kwargs.get('auto_validate', False)
        self.__validate_response = kwargs.get('validate_response', False)
        self.__resolver = Resolver(**kwargs)
        self.__validator = Validator(**kwargs)

    def auto_load(self):
        self.__resolver.auto_load()
        self.__validator.auto_load()

    def route(self, event, context):
        request = Request(event, context, self.__timeout)
        response = Response(cors=self.__cors)
        try:
            self.__log_verbose(title='request-received', log={'request': request})
            self.__run_route_procedure(request, response)
        except ApiTimeOutException as timeout_error:
            kwargs = {'code': timeout_error.code, 'key_path': timeout_error.key_path, 'message': timeout_error.message, 'error': timeout_error}
            self.__handle_error(request, response, self.__on_timeout, **kwargs)
        except ApiException as api_error:
            kwargs = {'code': api_error.code, 'key_path': api_error.key_path, 'message': api_error.message, 'error': api_error}
            self.__handle_error(request, response, self.__on_error, **kwargs)
        except Exception as error:
            output = str(error) if self.__output_error else 'internal service error'
            kwargs = {'code': 500, 'key_path': 'unknown', 'message': output, 'error': error}
            self.__handle_error(request, response, **kwargs)
        self.__log_verbose(title='request-processed', log={'request': request, 'response': response})
        return response.full

    def __run_route_procedure(self, request, response):
        endpoint = self.__resolver.get_endpoint(request)
        self.__run_before_all(request, response, endpoint)
        self.__run_with_auth(request, response, endpoint)
        self.__run_request_validation(request, response, endpoint)
        if not response.has_errors:
            endpoint.run(request, response)
        self.__run_response_validation(request, response, endpoint)
        self.__run_after_all(request, response, endpoint)
        return response

    def __run_before_all(self, request, response, endpoint):
        if not response.has_errors and self.__before_all and callable(self.__before_all):
            self.__before_all(request, response, endpoint.requirements)

    def __run_with_auth(self, request, response, endpoint):
        if not response.has_errors and self.__with_auth and callable(self.__with_auth):
            if (self.__auto_validate and self.__validator.request_has_security(request)) or endpoint.requires_auth:
                self.__with_auth(request, response, endpoint.requirements)

    def __run_request_validation(self, request, response, endpoint):
        if not response.has_errors and self.__auto_validate:
            self.__validator.validate_request_with_openapi(request, response)
        elif not response.has_errors and endpoint.has_requirements:
            self.__validator.validate_request(request, response, endpoint.requirements)

    def __run_response_validation(self, request, response, endpoint):
        if not response.has_errors and self.__auto_validate and self.__validate_response:
            self.__validator.validate_response_with_openapi(request, response)
        elif not response.has_errors and self.__validate_response and endpoint.has_required_response:
            self.__validator.validate_response(response, endpoint.requirements)

    def __run_after_all(self, request, response, endpoint):
        if not response.has_errors and self.__after_all and callable(self.__after_all):
            self.__after_all(request, response, endpoint.requirements)

    def __handle_error(self, request, response, error_func=None, **kwargs):
        try:
            response.code = kwargs['code']
            response.set_error(key_path=kwargs['key_path'], message=kwargs['message'])
            if error_func and callable(error_func):
                error_func(request, response, kwargs.get('error'))
            else:
                logger.log(level='ERROR', log={'request': request, 'response': response, 'error': kwargs})
        except Exception as exception:
            logging.exception(exception)

    def __log_verbose(self, title, log):
        if self.__verbose:
            logger.log(level='INFO', log={'title': title, 'log': log})
