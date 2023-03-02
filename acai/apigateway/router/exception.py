class RouteException(Exception):

    def __init__(self, **kwargs):
        self.code = kwargs.get('code', 404)
        self.key_path = kwargs.get('key_path', 'unknown')
        self.message = kwargs.get('message', 'unknown route resolver error')
        super().__init__(self.message)
