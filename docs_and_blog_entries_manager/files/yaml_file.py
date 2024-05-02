import codecs

import yaml


def load_yaml(file_path):
    with codecs.open(file_path, 'r', 'utf-8') as file:
        obj = yaml.safe_load(file)
    return obj
