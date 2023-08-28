from datetime import datetime

from acai_aws.common import logger
from acai_aws.base.record import BaseRecord


class Record(BaseRecord):

    def __init__(self, event):
        super().__init__(event)
        self._event = event.get('event')
        self.mongo_operations = {
            'create': self.CREATED,
            'createIndexes': self.CREATED,
            'delete': self.DELETED,
            'drop': self.DELETED,
            'dropDatabase': self.DELETED,
            'dropIndexes': self.DELETED,
            'insert': self.CREATED,
            'invalidate': self.DELETED,
            'modify': self.UPDATED,
            'rename': self.UPDATED,
            'update': self.UPDATED,
            'shardCollection': self.CREATED
        }

    @property
    def event_id(self):
        return self._event.get('_id', {}).get('_data')

    @property
    def cluster_time(self):
        time_stamp = self._event.get('clusterTime', {}).get('$timestamp', {})
        time = time_stamp.get('t')
        zone = time_stamp.get('i')
        return datetime.fromtimestamp(float(f'{time}.{zone}')).isoformat()

    @property
    def document_key(self):
        return self._event.get('documentKey', {}).get('_id', {}).get('$oid')

    @property
    def full_document(self):
        return self._event.get('fullDocument', {})

    @property
    def body(self):
        body = self.full_document.copy()
        body['id'] = self.full_document['_id']['$oid']
        del body['_id']
        return body

    @property
    def operation(self):
        try:
            return self.mongo_operations[self.change_event]
        except Exception as error:
            logger.log(level='ERROR', log={'event': self._event, 'error': error})
            return self.UNKNOWN

    @property
    def change_event(self):
        return self._event.get('operationType', 'unknown')

    @property
    def db(self):
        return self._event.get('ns', {}).get('db')

    @property
    def collection(self):
        return self._event.get('ns', {}).get('coll')

    def __str__(self):
        return str({
            'event_id': self.event_id,
            'cluster_time': self.cluster_time,
            'document_key': self.document_key,
            'operation': self.operation,
            'full_document': self.full_document,
            'db': self.db,
            'collection': self.collection
        })
