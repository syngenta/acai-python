from acai.common.json_helper import JsonHelper
from acai.base.no_data import NoDataClass


# noinspection PyArgumentList
class Event:

    def __init__(self, event, context=None):
        self._event = event
        self._context = context
        self.__data_class = NoDataClass

    @property
    def body(self):
        body = JsonHelper.decode(self._event)
        if self.data_class:
            return self.data_class(event=body)
        return body

    @property
    def data_class(self):
        if issubclass(self.__data_class, NoDataClass):
            return None
        return self.__data_class

    @data_class.setter
    def data_class(self, data_class):
        self.__data_class = data_class
