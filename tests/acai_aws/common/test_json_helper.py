import unittest

from acai_aws.common.json_helper import JsonHelper


class JsonHelperTest(unittest.TestCase):

    def setUp(self):
        self.valid_json = '{"key": "value"}'
        self.valid_dict = {'key': 'value'}
        self.invalid_json = '{"key": "value"}{'
        self.invalid_dict = {'key', 'value'}

    def test_decode(self):
        valid_dict = JsonHelper.decode(self.valid_json)
        self.assertDictEqual(valid_dict, self.valid_dict)

    def test_decode_invalid(self):
        invalid_json = JsonHelper.decode(self.invalid_json)
        self.assertEqual(invalid_json, self.invalid_json)

    def test_decode_invalid_raise_error(self):
        try:
            JsonHelper.decode(self.invalid_json, True)
            fail = True
        except:
            fail = False
        if fail:
            self.fail('didnt raise error')

    def test_encode(self):
        valid_json = JsonHelper.encode(self.valid_dict)
        self.assertEqual(valid_json, self.valid_json)

    def test_encode_invalid(self):
        invalid = JsonHelper.encode(self.invalid_dict)
        self.assertEqual(invalid, self.invalid_dict)

    def test_encode_invalid_raise_error(self):
        try:
            invalid_json = JsonHelper.encode(self.invalid_dict, True)
            fail = True
        except:
            fail = False
        if fail:
            self.fail('didnt raise error')
