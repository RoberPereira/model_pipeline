import json
import os


class Struct:
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            if isinstance(value, dict):
                self.__dict__[key] = Struct(**value)
            else:
                self.__dict__[key] = value


with open('etl/config.json', 'r') as config_file:
    config = Struct(**json.load(config_file))

if __name__ == '__main__':
    # current_directory = os.path.dirname(os.path.realpath(__file__))
    # config_path = os.path.join(current_directory, 'config.json')

    current_dir = os.path.dirname(os.path.relpath('__file__'))
    print(config)
