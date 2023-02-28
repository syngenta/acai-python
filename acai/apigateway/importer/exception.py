class ImporterException(Exception):

    def __init__(self, **kwargs):
        self.message = kwargs.get('message', 'unknown importer error')
        super().__init__(self.message)
