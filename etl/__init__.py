import json
import os
from src.utils.util import DotDict


current_dir = os.path.dirname(os.path.abspath('__file__'))
if 'notebook' in current_dir:
    # Set home path
    current_dir = os.path.dirname(current_dir)


with open(current_dir+'/etl/config.json', 'r') as config_file:
    config = DotDict(**json.load(config_file))
