class Endpoint:
    def __init__(self, module, method):
        self.__method = getattr(module, method)
        self.__requirements = getattr(self.__method, 'requirements', {})

    @property
    def has_requirements(self):
        return bool(self.__requirements)

    @property
    def requirements(self):
        return self.__requirements

    @property
    def requires_auth(self):
        return self.__requirements.get('auth_required')

    @property
    def has_required_response(self):
        return bool(self.__requirements.get('required_response'))

    @property
    def has_required_route(self):
        return bool(self.__requirements.get('required_route'))

    @property
    def required_route(self):
        return self.__requirements.get('required_route', '')

    def run(self, request, response):
        return self.__method(request, response)
