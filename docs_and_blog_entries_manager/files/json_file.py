import codecs
import json

from files.value.file_path import FilePath


def load(file_path: FilePath):
    if not file_path.exist():
        return {}
    with codecs.open(file_path.value, mode='r', encoding='utf-8') as file:
        obj = json.load(file)
    return obj


def save(file_path: FilePath, dump_data):
    with codecs.open(file_path.value, mode='w', encoding='utf-8') as file:
        json.dump(dump_data, file, indent=2, ensure_ascii=False)
