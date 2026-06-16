from unittest import TestCase

from acai_aws.common.logger.redaction import redaction_filter
from acai_aws.common.logger.defaults import DEFAULT_PII_KEYS, DEFAULT_PII_PATTERNS


class RedactionFilterTest(TestCase):

    def test_redacts_matching_keys(self):
        callback = redaction_filter(keys=['email', 'last_name'])
        record = callback({'log': {'first_name': 'Ada', 'last_name': 'Lovelace', 'email': 'ada@example.com'}})
        self.assertEqual('Ada', record['log']['first_name'])
        self.assertEqual('[REDACTED]', record['log']['last_name'])
        self.assertEqual('[REDACTED]', record['log']['email'])

    def test_key_match_is_case_insensitive(self):
        callback = redaction_filter(keys=['email'])
        record = callback({'log': {'Email': 'ada@example.com'}})
        self.assertEqual('[REDACTED]', record['log']['Email'])

    def test_redacts_nested_keys_in_dicts_and_lists(self):
        callback = redaction_filter(keys=['ssn'])
        payload = {'worker': {'ssn': '123-45-6789', 'id': 5}, 'items': [{'ssn': '111-22-3333'}]}
        record = callback({'log': payload})
        self.assertEqual('[REDACTED]', record['log']['worker']['ssn'])
        self.assertEqual(5, record['log']['worker']['id'])
        self.assertEqual('[REDACTED]', record['log']['items'][0]['ssn'])

    def test_redacts_value_patterns(self):
        callback = redaction_filter(patterns=[r'\b\d{3}-\d{2}-\d{4}\b'])
        record = callback({'log': {'note': 'ssn is 123-45-6789 today'}})
        self.assertEqual('ssn is [REDACTED] today', record['log']['note'])

    def test_custom_redact_with(self):
        callback = redaction_filter(keys=['email'], redact_with='')
        record = callback({'log': {'email': 'ada@example.com'}})
        self.assertEqual('', record['log']['email'])

    def test_leaves_non_matching_data_untouched(self):
        callback = redaction_filter(keys=['email'], patterns=[r'\b\d{3}-\d{2}-\d{4}\b'])
        record = callback({'log': {'count': 3, 'ok': True, 'name': 'service-payroll'}})
        self.assertEqual({'count': 3, 'ok': True, 'name': 'service-payroll'}, record['log'])

    def test_handles_record_without_log_key(self):
        callback = redaction_filter(keys=['email'])
        record = callback({'level': 'INFO'})
        self.assertEqual({'level': 'INFO'}, record)

    def test_default_pii_keys_and_patterns(self):
        callback = redaction_filter(keys=DEFAULT_PII_KEYS, patterns=DEFAULT_PII_PATTERNS)
        record = callback({'log': {
            'first_name': 'Ada',
            'worker_email': 'ada@example.com',
            'ein': '12-3456789',
            'message': 'call 585-555-1234 or email ada@example.com',
        }})
        log = record['log']
        self.assertEqual('[REDACTED]', log['first_name'])
        self.assertEqual('[REDACTED]', log['worker_email'])
        self.assertEqual('[REDACTED]', log['ein'])
        self.assertNotIn('585-555-1234', log['message'])
        self.assertNotIn('ada@example.com', log['message'])
