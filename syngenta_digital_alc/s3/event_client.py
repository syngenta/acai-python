from syngenta_digital_alc.s3.record_client import RecordClient


class EventClient:

    def __init__(self, event, context):
        self._event = event
        self.context = context

    @property
    def records(self):
        return [RecordClient(record) for record in self._event.get('Records', [])]

    @property
    def raw_records(self):
        return self._event.get('Records', [])

    def __str__(self):
        return str([str(record) for record in self.records])
