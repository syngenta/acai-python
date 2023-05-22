import inspect

from acai.common import logger
from acai.common.records.exception import EventException
from acai.common.records.event import CommonRecordsEvent
from acai.documentdb.event import Event as DocumentDBEvent
from acai.dynamodb.event import Event as DynamoDBEvent
from acai.firehose.event import Event as FirehoseEvent
from acai.kinesis.event import Event as KinesisEvent
from acai.s3.event import Event as S3Event
from acai.sns.event import Event as SNSEvent
from acai.sqs.event import Event as SQSEvent


def requirements(**kwargs):

    def __find_event_source(event):
        if event.get('eventSource'):
            return event['eventSource']
        if event.get('deliveryStreamArn'):
            return event['deliveryStreamArn']
        if event.get('Records') and event['Records'][0].get('eventSource'):
            return event['Records'][0]['eventSource']
        if event.get('Records') and event['Records'][0].get('EventSource'):
            return event['Records'][0]['EventSource']
        raise EventException(message='no known record event source found')

    def __determine_event_type(event, context):
        event_clients = {
            'unknown': CommonRecordsEvent,
            'aws:docdb': DocumentDBEvent,
            'aws:dynamodb': DynamoDBEvent,
            'aws:lambda:events': FirehoseEvent,
            'aws:kinesis': KinesisEvent,
            'aws:s3': S3Event,
            'aws:sns': SNSEvent,
            'aws:sqs': SQSEvent
        }
        try:
            source = __find_event_source(event)
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
