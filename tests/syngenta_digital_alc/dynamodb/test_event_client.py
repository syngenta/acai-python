import unittest

from tests.syngenta_digital_alc.dynamodb import mock_data
from syngenta_digital_alc.dynamodb.event_client import EventClient
from syngenta_digital_alc.dynamodb.record_client import RecordClient


class EventClientTest(unittest.TestCase):

    def test_ddb_record(self):
        client = EventClient(mock_data.get_ddb_event(), None)
        ddb_record = client.records[0]
        self.assertIsInstance(ddb_record, RecordClient)

    def test_ddb_doesnt_parse_record(self):
        client = EventClient(mock_data.get_ddb_event(), None)
        self.assertDictEqual(
            client.records[0]._record,
            mock_data.get_ddb_event()['Records'][0]
        )

    def test_ddb_record_parse_image(self):
        client = EventClient(mock_data.get_ddb_event(), None)
        self.assertDictEqual(
            client.records[0].new_image,
            {
                'example_id': '123456789',
                'note': "Hosrawguw verrig zogupap ce so fajdis vub mos sif mawpowpug kif kihane.",
                'active': True,
                'personal': {
                    'gender': 'male',
                    'last_name': 'Mcneil',
                    'first_name': 'Mannix',
                },
                'transportation': [
                    'public-transit',
                    'car-access',
                ]
            }
        )
