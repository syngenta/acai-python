import inspect

from acai.s3.records_event import RecordsEvent


def requirements(**kwargs):
    def decorator_func(func):

        def run_before(records_event):
            if kwargs.get('before') and callable(kwargs['before']):
                kwargs['before'](records_event, kwargs)

        def run_after(records_event, result):
            if kwargs.get('after') and callable(kwargs['after']):
                kwargs['after'](records_event, result, kwargs)

        def run_function(aws_event, aws_context):
            records_event = RecordsEvent(aws_event, aws_context, **kwargs)
            run_before(records_event)
            if kwargs.get('data_class') and inspect.isclass(kwargs['data_class']):
                records_event.data_class = kwargs['data_class']
            result = func(records_event)
            run_after(records_event, result)
            return result

        return run_function

    return decorator_func
