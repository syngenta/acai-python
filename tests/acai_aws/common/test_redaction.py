from unittest import TestCase

from acai_aws.common.logger.redaction import RedactionFilter


class RedactionFilterTest(TestCase):

    def test_redacts_matching_keys(self):
        redact = RedactionFilter(keys=['email', 'last_name'])
        record = redact({'log': {'first_name': 'Ada', 'last_name': 'Lovelace', 'email': 'ada@example.com'}})
        self.assertEqual('Ada', record['log']['first_name'])
        self.assertEqual('[REDACTED]', record['log']['last_name'])
        self.assertEqual('[REDACTED]', record['log']['email'])

    def test_key_match_is_case_insensitive(self):
        redact = RedactionFilter(keys=['email'])
        record = redact({'log': {'Email': 'ada@example.com'}})
        self.assertEqual('[REDACTED]', record['log']['Email'])

    def test_redacts_nested_keys_in_dicts_and_lists(self):
        redact = RedactionFilter(keys=['ssn'])
        payload = {'worker': {'ssn': '123-45-6789', 'id': 5}, 'items': [{'ssn': '111-22-3333'}]}
        record = redact({'log': payload})
        self.assertEqual('[REDACTED]', record['log']['worker']['ssn'])
        self.assertEqual(5, record['log']['worker']['id'])
        self.assertEqual('[REDACTED]', record['log']['items'][0]['ssn'])

    def test_redacts_value_patterns(self):
        redact = RedactionFilter(patterns=[r'\b\d{3}-\d{2}-\d{4}\b'])
        record = redact({'log': {'note': 'ssn is 123-45-6789 today'}})
        self.assertEqual('ssn is [REDACTED] today', record['log']['note'])

    def test_custom_redact_with(self):
        redact = RedactionFilter(keys=['email'], redact_with='')
        record = redact({'log': {'email': 'ada@example.com'}})
        self.assertEqual('', record['log']['email'])

    def test_leaves_non_matching_data_untouched(self):
        redact = RedactionFilter(keys=['email'], patterns=[r'\b\d{3}-\d{2}-\d{4}\b'])
        record = redact({'log': {'count': 3, 'ok': True, 'name': 'service-payroll'}})
        self.assertEqual({'count': 3, 'ok': True, 'name': 'service-payroll'}, record['log'])

    def test_handles_record_without_log_key(self):
        redact = RedactionFilter(keys=['email'])
        record = redact({'level': 'INFO'})
        self.assertEqual({'level': 'INFO'}, record)

    def test_keys_and_patterns_together(self):
        redact = RedactionFilter(
            keys=['first_name', 'email'],
            patterns=[r'\b\d{3}-\d{2}-\d{4}\b', r'[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}'],
        )
        record = redact({'log': {
            'first_name': 'Ada',
            'email': 'ada@example.com',
            'message': 'ssn 123-45-6789 mailto ada@example.com',
        }})
        log = record['log']
        self.assertEqual('[REDACTED]', log['first_name'])
        self.assertEqual('[REDACTED]', log['email'])
        self.assertNotIn('123-45-6789', log['message'])
        self.assertNotIn('ada@example.com', log['message'])
