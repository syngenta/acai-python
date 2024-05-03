class HandlerModule:
    
    def __init__(self, file_path):
        self.__file_path = file_path

    @classmethod
    def convert_from_file_paths(cls, file_paths):
        # SUPPORTED_METHODS = ['any', 'delete', 'get', 'head', 'options', 'patch', 'post', 'put']
        modules = []
        for file in file_paths:
            modules.append(cls(file))
        return modules

    @property
    def operation_id(self):
        pass

    @property
    def path(self):
        # required_route overwrites this logic
        pass

    @property
    def method(self):
        pass

    @property
    def required_auth(self):
        pass

    @property
    def required_headers(self):
        pass

    @property
    def available_headers(self):
        pass

    @property
    def required_query(self):
        pass

    @property
    def available_query(self):
        pass

    @property
    def request_body(self):
        pass

    @property
    def response_body(self):
        pass
