from acai.apigateway.resolver.modes.base import BaseModeResolver


class PatternModeResolver(BaseModeResolver):

    def __init__(self, **kwargs):  # pylint: disable=unused-private-member
        super().__init__(**kwargs)
        self.__handler_pattern = kwargs['handlers']

    def _get_file_and_import_path(self, request_path):
        pass
