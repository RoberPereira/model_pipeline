import json
from src.utils.util import DotDict

with open('train/config.json', 'r') as config_file:
    config = DotDict(**json.load(config_file))

etl_version = config.etl_version
with open(f'etl/metadata/metadata_v{etl_version}.json', 'r') as metadata:
    etl_metadata = DotDict(**json.load(metadata))

with open(f'etl/metadata/metadata_v{etl_version}.json', 'r') as metadata:
    etl_metadata_serialized = json.load(metadata)
