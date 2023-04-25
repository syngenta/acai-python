import abc

class BaseRecordsEvent(abc.ABC):

    def __init__(self, event, context):
        self._event = event
        self._context = context
        self.data_class = None

    @property
    def event(self):
        return self._event

    @property
    def context(self):
        return self._context

    @property
    def raw_records(self):
        return self._event.get('Records', [])

    @abc.abstractmethod
    @property
    def records(self):
        raise NotImplementedError

    @abc.abstractmethod
    @property
    def data_classes(self):
        raise NotImplementedError

    def __str__(self):
        return str([str(record) for record in self.records])
