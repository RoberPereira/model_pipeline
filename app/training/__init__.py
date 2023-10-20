import json
import os


current_directory = os.path.dirname(os.path.realpath(__file__))
config_path = os.path.join(current_directory, 'config.json')

with open(config_path, 'r') as config_file:
    train_config = json.load(config_file)


if __name__ == '__main__':
    current_dir = os.path.dirname(os.path.relpath('__file__'))
    print(train_config)
