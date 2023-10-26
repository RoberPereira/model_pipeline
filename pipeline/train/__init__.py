import os

current_dir = os.path.dirname(os.path.abspath('__file__'))
if 'notebook' in current_dir:
    # Set home path
    current_dir = os.path.dirname(current_dir)


