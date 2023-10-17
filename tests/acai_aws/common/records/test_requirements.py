import unittest

from acai_aws.common.records.exception import EventTimeOutException

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

from tests.mocks.documentdb import mock_event as mock_docdb
from tests.mocks.dynamodb import mock_event as mock_ddb
from tests.mocks.firehose import mock_event as mock_firehose
from tests.mocks.kinesis import mock_event as mock_kinesis
from tests.mocks.msk import mock_event as mock_msk
from tests.mocks.mq import mock_event as mock_mq
from tests.mocks.s3 import mock_event as mock_s3
from tests.mocks.sns import mock_event as mock_sns
from tests.mocks.sqs import mock_event as mock_sqs

from tests.mocks.common.mock_functions import mock_func_verbose, mock_func_timeout


class CommonRequirementsTest(unittest.TestCase):
    context = None
    unknown_event = {'unknown': 'value'}
    docdb_event = mock_docdb.get_basic()
    ddb_event = mock_ddb.get_created_event()
    firehose_event = mock_firehose.get_basic()
    kinesis_event = mock_kinesis.get_basic()
    msk_event = mock_msk.get_basic()
    mq_event = mock_mq.get_basic()
    s3_event = mock_s3.get_basic()
    sns_event = mock_sns.get_basic()
    sqs_event = mock_sqs.get_basic()

    def test_decorator_with_unknown_event(self):
        result = mock_func_verbose(self.unknown_event, self.context)
        self.assertTrue(isinstance(result, CommonEvent))

    def test_decorator_with_docdb_event(self):
        result = mock_func_verbose(self.docdb_event, self.context)
        self.assertTrue(isinstance(result, DocumentDBEvent))

    def test_decorator_with_ddb_event(self):
        result = mock_func_verbose(self.ddb_event, self.context)
        self.assertTrue(isinstance(result, DynamoDBEvent))

    def test_decorator_with_firehose_event(self):
        result = mock_func_verbose(self.firehose_event, self.context)
        self.assertTrue(isinstance(result, FirehoseEvent))

    def test_decorator_with_kinesis_event(self):
        result = mock_func_verbose(self.kinesis_event, self.context)
        self.assertTrue(isinstance(result, KinesisEvent))

    def test_decorator_with_msk_event(self):
        result = mock_func_verbose(self.msk_event, self.context)
        self.assertTrue(isinstance(result, MSKEvent))

    def test_decorator_with_mq_event(self):
        result = mock_func_verbose(self.mq_event, self.context)
        self.assertTrue(isinstance(result, MQEvent))

    def test_decorator_with_s3_event(self):
        result = mock_func_verbose(self.s3_event, self.context)
        self.assertTrue(isinstance(result, S3Event))

    def test_decorator_with_sns_event(self):
        result = mock_func_verbose(self.sns_event, self.context)
        self.assertTrue(isinstance(result, SNSEvent))

    def test_decorator_with_sqs_event(self):
        result = mock_func_verbose(self.sqs_event, self.context)
        self.assertTrue(isinstance(result, SQSEvent))

    def test_decorator_with_timeout(self):
        try:
            mock_func_timeout(self.sqs_event, self.context)
            self.assertTrue(False)
        except EventTimeOutException as error:
            self.assertTrue(isinstance(error, EventTimeOutException))
