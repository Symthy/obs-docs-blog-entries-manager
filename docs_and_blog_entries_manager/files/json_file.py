import codecs
import json

from docs_and_blog_entries_manager.files import file_system


def load(file_path):
    if not file_system.exist_file(file_path):
        return {}
    with codecs.open(file_path, mode='r', encoding='utf-8') as file:
        obj = json.load(file)
    return obj


def save(file_path, dump_data):
    with codecs.open(file_path, mode='w', encoding='utf-8') as file:
        json.dump(dump_data, file, indent=2, ensure_ascii=False)
