from syngenta_digital_alc.dynamodb.record_client import RecordClient


class EventClient:
    
    def __init__(self, event):
        self._event = event

    @property
    def records(self):
        return [RecordClient(record) for record in self._event['Records']]

    @property
    def raw_records(self):
        return self._event['Records']

    def __str__(self):
        return str([str(record) for record in self.records])
