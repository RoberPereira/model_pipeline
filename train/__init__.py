import json


class Struct:
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            if isinstance(value, dict):
                self.__dict__[key] = Struct(**value)
            else:
                self.__dict__[key] = value


with open('train/config.json', 'r') as config_file:
    config = Struct(**json.load(config_file))

etl_version = config.etl_version
with open(f'etl/metadata/metadata_v{etl_version}.json', 'r') as metadata:
    etl_metadata = Struct(**json.load(metadata))
