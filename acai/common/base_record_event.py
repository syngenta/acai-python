import abc


class BaseRecordEvent(abc.ABC):
    CREATED = 'created'
    UPDATED = 'updated'
    DELETED = 'deleted'
    UNKNOWN = 'unknown'

    def __init__(self, record):
        self.valid = True
        self._body = None
        self._record = record

    @property
    @abc.abstractmethod
    def body(self):
        raise NotImplementedError

    @body.setter
    @abc.abstractmethod
    def body(self, _):
        raise NotImplementedError

    @property
    @abc.abstractmethod
    def operations(self):
        raise NotImplementedError
