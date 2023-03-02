class ResolveException(Exception):

    def __init__(self, **kwargs):
        self.code = kwargs.get('code', 404)
        self.message = kwargs.get('message', 'unknown resolver error')
        super().__init__(self.message)
