class RecordException(Exception):

    def __init__(self, **kwargs):
        self.record = kwargs.get('record', {})
        self.message = kwargs.get('message', 'record error')
        super().__init__(self.message)


class EventException(Exception):

    def __init__(self, **kwargs):
        self.message = kwargs.get('message', 'event error')
        super().__init__(self.message)
