class ApiException(Exception):

    def __init__(self, **kwargs):
        self.code = kwargs.get('code', 500)
        self.key_path = kwargs.get('key_path', 'unknown')
        self.message = kwargs.get('message', 'internal server error')
        super().__init__(self.message)
