class Endpoint:

    def __init__(self, module, method):
        self.__endpoint_method = getattr(module, method)
        self.__requirements = getattr(module, 'requirements', {})

    @property
    def has_requirements(self):
        return bool(self.__requirements)

    @property
    def requirements(self):
        return self.__requirements

    @property
    def requires_auth(self):
        return self.__requirements.get('auth_required', False)

    def run(self, request, response):
        return self.__endpoint_method(request, response)
