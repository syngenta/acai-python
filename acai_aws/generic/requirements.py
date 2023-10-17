import inspect
import signal

from acai_aws.generic.event import Event
from acai_aws.common.records.exception import EventTimeOutException


def requirements(**kwargs):

    def decorator_func(func):

        def raise_timeout(*_):
            raise EventTimeOutException
        
        def start_timeout():
            if kwargs.get('timeout') is not None:
                signal.signal(signal.SIGALRM, raise_timeout)
                signal.alarm(kwargs['timeout'])
        
        def end_timeout():
            signal.alarm(0)

        def run_before(generic_event):
            if kwargs.get('before') and callable(kwargs['before']):
                kwargs['before'](generic_event, kwargs)

        def run_after(generic_event, result):
            if kwargs.get('after') and callable(kwargs['after']):
                kwargs['after'](generic_event, result, kwargs)

        def run_function(event, context):
            generic_event = Event(event, context)
            run_before(generic_event)
            if kwargs.get('data_class') and inspect.isclass(kwargs['data_class']):
                generic_event = kwargs['data_class'](event=generic_event)
            start_timeout()
            result = func(generic_event)
            end_timeout()
            run_after(generic_event, result)
            return result

        return run_function

    return decorator_func
