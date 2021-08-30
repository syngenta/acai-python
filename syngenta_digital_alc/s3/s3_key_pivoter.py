import os

import re


class S3KeyPivoter:

    @staticmethod
    def extract_operation_id_from_filename(filename):
        uuid_pattern = r'^[0-9a-fA-F]{8}\b-[0-9a-fA-F]{4}\b-[0-9a-fA-F]{4}\b-[0-9a-fA-F]{4}\b-[0-9a-fA-F]{12}'
        return re.match(pattern=uuid_pattern, string=filename).group()

    @classmethod
    def parse_key(cls, key):
        data_stage, account_id, entity, filename = key.strip('/').split('/')
        operation_id = cls.extract_operation_id_from_filename(filename)

        return cls(
            data_stage=data_stage,
            account_id=account_id,
            entity=entity,
            operation_id=operation_id
        )

    def __init__(self, data_stage: str, account_id: str, entity: str, operation_id: str):
        self.data_stage = data_stage
        self.account_id = account_id
        self.entity = entity
        self.operation_id = operation_id

    def __base_key(self, **kwargs):
        defaults = {
            'data_stage': self.data_stage,
            'account_id': self.account_id,
            'entity': self.entity,
            'operation_id': self.operation_id
        }

        inputs = {**defaults, **kwargs}

        return "{data_stage}/{account_id}/{entity}/{operation_id}".format(**inputs)

    def file_summary(self, **kwargs):
        return f"{self.__base_key(**kwargs)}-summary.json"

    def file_spatial(self, **kwargs):
        return f"{self.__base_key(**kwargs)}-spatial.geojson"

    def file_rectangular_unbuffered(self, **kwargs):
        return f"{self.__base_key(**kwargs)}-rectangular-unbuffered.geojson"

    def file_rectangular_unbuffered_downsampled(self, **kwargs):
        return f"{self.__base_key(**kwargs)}-rectangular-unbuffered-downsampled.geojson"

    def file_buffered(self, **kwargs):
        return f"{self.__base_key(**kwargs)}-rectangular-buffered.geojson"



