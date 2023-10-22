import json
import os
from src.utils.util import DotDict

current_dir = os.path.dirname(os.path.abspath('__file__'))
if 'notebook' in current_dir:
    # Set home path
    current_dir = os.path.dirname(current_dir)

with open(current_dir+'/train/config.json', 'r') as config_file:
    config = DotDict(**json.load(config_file))

etl_version = config.etl_version
with open(f'{current_dir}/etl/metadata/metadata_v{etl_version}.json',
          'r') as metadata:
    etl_metadata = DotDict(**json.load(metadata))

with open(f'{current_dir}/etl/metadata/metadata_v{etl_version}.json',
          'r') as metadata:
    etl_metadata_serialized = json.load(metadata)
