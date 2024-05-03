class HandlerModule:
    
    def __init__(self, file_path, module, method):
        self.__module = module
        self.__file_path = file_path
        self.__method = method

    @property
    def file_path(self):
        return self.__file_path
    
    @property
    def module(self):
        return self.__module
    
    @property
    def method(self):
        return self.__method

    @property
    def operation_id(self):
        pass

    @property
    def route_path(self):
        # required_route overwrites this logic
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
