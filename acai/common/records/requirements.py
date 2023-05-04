import inspect

from acai.common import logger
from acai.common.records.event import CommonRecordsEvent
from acai.s3.event import Event as S3Event
from acai.dynamodb.event import Event as DynamoDBEvent


def requirements(**kwargs):

    def __determine_event_type(event, context):
        event_clients = {
            'unknown': CommonRecordsEvent,
            'aws:s3': S3Event,
            'aws:dynamodb': DynamoDBEvent
        }
        try:
            source = event['Records'][0]['eventSource']
            return event_clients[source](event, context, **kwargs)
        except Exception as error:
            if kwargs.get('verbose'):
                logger.log(level='ERROR', log={'event': event, 'context': context, 'error': error})
            return event_clients['unknown'](event, context, **kwargs)

    def decorator_func(func):

        def run_before(records_event):
            if kwargs.get('before') and callable(kwargs['before']):
                kwargs['before'](records_event, kwargs)

        def run_after(records_event, result):
            if kwargs.get('after') and callable(kwargs['after']):
                kwargs['after'](records_event, result, kwargs)

        def run_function(event, context):
            records_event = __determine_event_type(event, context)
            run_before(records_event)
            if kwargs.get('data_class') and inspect.isclass(kwargs['data_class']):
                records_event.data_class = kwargs['data_class']
            result = func(records_event)
            run_after(records_event, result)
            return result

        return run_function

    return decorator_func
