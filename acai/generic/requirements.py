import inspect

from acai.generic.event import Event


def requirements(**kwargs):

    def decorator_func(func):

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
                generic_event.data_class = kwargs['data_class']
            result = func(generic_event)
            run_after(generic_event, result)
            return result

        return run_function

    return decorator_func
