class Endpoint:

    def __init__(self, module, method):
        self.__endpoint_method = getattr(module, method)
        self.__requirements = getattr(self.__endpoint_method, 'requirements', {})

    @property
    def has_requirements(self):
        return bool(self.__requirements)

    @property
    def requirements(self):
        return self.__requirements

    @property
    def requires_auth(self):
        return self.__requirements.get('auth_required', False)

    @property
    def has_required_route(self):
        return bool(self.__requirements.get('required_route'))

    @property
    def required_route(self):
        return self.__requirements.get('required_route', '')

    def run(self, request, response):
        return self.__endpoint_method(request, response)
