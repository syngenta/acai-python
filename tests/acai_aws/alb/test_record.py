import unittest

from acai_aws.alb.record import Record

from tests.mocks.alb import mock_event


class ALBRecordTest(unittest.TestCase):
    basic_event = mock_event.get_basic()
    base64_event = mock_event.get_base64()

    def test_record_body_parsed_from_json(self):
        record = Record(self.basic_event)
        self.assertEqual(record.body['business_id'], 'biz-e2e-001')
        self.assertEqual(record.body['decision'], 'APPROVED')
        self.assertEqual(record.body['completed'], '2026-03-30T12:40:40.353')

    def test_record_body_parsed_from_base64(self):
        record = Record(self.base64_event)
        self.assertEqual(record.body['business_id'], 'biz-e2e-002')
        self.assertEqual(record.body['decision'], 'DENIED')

    def test_record_operation_post_is_created(self):
        record = Record(mock_event.get_basic('POST'))
        self.assertEqual(record.operation, record.CREATED)

    def test_record_operation_put_is_updated(self):
        record = Record(mock_event.get_basic('PUT'))
        self.assertEqual(record.operation, record.UPDATED)

    def test_record_operation_patch_is_updated(self):
        record = Record(mock_event.get_basic('PATCH'))
        self.assertEqual(record.operation, record.UPDATED)

    def test_record_operation_delete_is_deleted(self):
        record = Record(mock_event.get_basic('DELETE'))
        self.assertEqual(record.operation, record.DELETED)

    def test_record_operation_get_is_unknown(self):
        record = Record(mock_event.get_basic('GET'))
        self.assertEqual(record.operation, record.UNKNOWN)

    def test_record_http_method(self):
        record = Record(self.basic_event)
        self.assertEqual(record.http_method, 'POST')

    def test_record_path(self):
        record = Record(self.basic_event)
        self.assertEqual(record.path, '/v1/kyc/callback')

    def test_record_headers(self):
        record = Record(self.basic_event)
        self.assertEqual(record.headers['content-type'], 'application/json')
        self.assertEqual(record.headers['host'], '10.84.140.68')

    def test_record_query_params(self):
        record = Record(self.basic_event)
        self.assertEqual(record.query_params['status'], 'approved')
        self.assertEqual(record.query_params['ref'], 'abc-123')

    def test_record_source_ip(self):
        record = Record(self.basic_event)
        self.assertEqual(record.source_ip, '10.104.8.48')

    def test_record_target_group_arn(self):
        record = Record(self.basic_event)
        self.assertEqual(
            record.target_group_arn,
            'arn:aws:elasticloadbalancing:us-east-1:123456789012:targetgroup/my-target-group/50dc6c495c0c9188'
        )

    def test_record_prints(self):
        try:
            record = Record(self.basic_event)
            print(record)
            self.assertTrue(True)
        except Exception as error:
            print(error)
            self.assertTrue(False)
