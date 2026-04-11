import inspect
import json
import signal

from acai_aws.base.event import FailureMode
from acai_aws.common import logger
from acai_aws.common.records.exception import EventException, EventTimeOutException
from acai_aws.alb.event import Event as ALBEvent
from acai_aws.common.records.event import Event as CommonEvent
from acai_aws.documentdb.event import Event as DocumentDBEvent
from acai_aws.dynamodb.event import Event as DynamoDBEvent
from acai_aws.firehose.event import Event as FirehoseEvent
from acai_aws.kinesis.event import Event as KinesisEvent
from acai_aws.msk.event import Event as MSKEvent
from acai_aws.mq.event import Event as MQEvent
from acai_aws.s3.event import Event as S3Event
from acai_aws.sns.event import Event as SNSEvent
from acai_aws.sqs.event import Event as SQSEvent


def requirements(**kwargs):

    def __find_event_source(event):
        if event.get('requestContext', {}).get('elb'):
            return 'aws:elb'
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
            'unknown': CommonEvent,
            'aws:docdb': DocumentDBEvent,
            'aws:dynamodb': DynamoDBEvent,
            'aws:elb': ALBEvent,
            'aws:lambda:events': FirehoseEvent,
            'aws:kafka': MSKEvent,
            'aws:mq': MQEvent,
            'aws:kinesis': KinesisEvent,
            'aws:s3': S3Event,
            'aws:sns': SNSEvent,
            'aws:sqs': SQSEvent
        }
        try:
            source = __find_event_source(event)
            return event_clients[source](event, context, **kwargs)
        except EventException as event_error:
            if kwargs.get('verbose'):
                logger.log(level='ERROR', log={'event': event, 'context': context, 'error': event_error})
            return event_clients['unknown'](event, context, **kwargs)

    def decorator_func(func):

        def raise_timeout(*_):
            raise EventTimeOutException

        def start_timeout():
            if kwargs.get('timeout') is not None:
                signal.signal(signal.SIGALRM, raise_timeout)
                signal.alarm(kwargs['timeout'])

        def end_timeout():
            signal.alarm(0)

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
            start_timeout()
            records_event.validate()
            short_circuit = records_event.build_short_circuit_response()
            if short_circuit is not None:
                end_timeout()
                return short_circuit
            result = func(records_event)
            end_timeout()
            run_after(records_event, result)
            if records_event.resolve_failure_mode() == FailureMode.RETURN_FAILURE:
                result = _merge_batch_item_failures(result, records_event)
            return result

        return run_function

    return decorator_func


def _merge_batch_item_failures(result, records_event):
    framework_failures = records_event.batch_item_failures()
    if not framework_failures:
        return result
    key = records_event.batch_failure_response_key
    existing = []
    if isinstance(result, dict) and isinstance(result.get(key), list):
        existing = list(result[key])
    seen = {json.dumps(item, sort_keys=True) for item in existing if isinstance(item, dict)}
    merged = list(existing)
    for failure in framework_failures:
        if json.dumps(failure, sort_keys=True) not in seen:
            merged.append(failure)
            seen.add(json.dumps(failure, sort_keys=True))
    if isinstance(result, dict):
        return {**result, key: merged}
    return {key: merged}
