import inspect

from acai.common.records import CommonRecords
from acai.s3.records import Records as S3Records
from acai.dynamodb.records import Records as DDBRecords


def requirements(**kwargs):
    records_client = {
        'aws:s3': S3Records,
        'aws:dynamodb': DDBRecords
    }

    def decorator_func(func):

        def run_before(records_event):
            if kwargs.get('before') and callable(kwargs['before']):
                kwargs['before'](records_event, kwargs)

        def run_after(records_event, result):
            if kwargs.get('after') and callable(kwargs['after']):
                kwargs['after'](records_event, result, kwargs)

        def run_function(event, context):
            source = event['Records'][0]['eventSource']
            records_event = records_client[source](event, context, **kwargs)
            run_before(records_event)
            if kwargs.get('data_class') and inspect.isclass(kwargs['data_class']):
                records_event.data_class = kwargs['data_class']
            result = func(records_event)
            run_after(records_event, result)
            return result

        return run_function

    return decorator_func
