from components._pipeline import (Etl, Train)

import os

__all__ = [
    'Etl',
    'Train'
]

current_dir = os.path.dirname(os.path.abspath('__file__'))
if 'notebook' in current_dir:
    current_dir = os.path.dirname(current_dir)
