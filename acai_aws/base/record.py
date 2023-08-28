import abc


class BaseRecord(abc.ABC):
    CREATED = 'created'
    UPDATED = 'updated'
    DELETED = 'deleted'
    UNKNOWN = 'unknown'

    def __init__(self, record):
        self.valid = True
        self._body = None
        self._record = record
        self._attributes = {}

    @property
    @abc.abstractmethod
    def body(self):
        raise NotImplementedError

    @property
    @abc.abstractmethod
    def operation(self):
        raise NotImplementedError
