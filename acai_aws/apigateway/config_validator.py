from acai_aws.apigateway.exception import ApiException


class ConfigValidator:

    @staticmethod
    def validate(**kwargs):
        if not kwargs.get('base_path') or not isinstance(kwargs.get('base_path'), str):
            raise ApiException(code=500, message='base_path string is required')
        if not kwargs.get('handlers') or not isinstance(kwargs.get('handlers'), (str, dict)):
            raise ApiException(code=500, message='handlers is required; must be glob pattern string or dictionary mapping {route: file_path}')
        if kwargs.get('schema') and not isinstance(kwargs.get('schema'), (str, dict)):
            raise ApiException(code=500, message='schema should either be file path string or json-schema style dictionary')
        if kwargs.get('auto_validate') and not isinstance(kwargs.get('auto_validate'), bool):
            raise ApiException(code=500, message='auto_validate should be a boolean')
        if kwargs.get('validate_response') and not isinstance(kwargs.get('validate_response'), bool):
            raise ApiException(code=500, message='validate_response should be a boolean')
        if kwargs.get('cache_size') and not isinstance(kwargs.get('cache_size'), int) and kwargs.get('cache_size') is not None:
            raise ApiException(code=500, message='cache_size should be an int (0 for unlimited size) or None (to disable route caching)')
        if kwargs.get('cache_mode') and kwargs['cache_mode'] not in ('all', 'static-only', 'dynamic-only'):
            raise ApiException(code=500, message='cache_mode should be a string of the one of the following values: all, static-only, dynamic-only')
        if kwargs.get('verbose_logging') and not isinstance(kwargs.get('verbose_logging'), bool):
            raise ApiException(code=500, message='verbose_logging should be a boolean')
