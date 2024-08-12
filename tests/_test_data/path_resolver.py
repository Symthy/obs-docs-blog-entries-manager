import os

from files.value.file_path import DirectoryPath


def resolve_test_data_dir_path() -> DirectoryPath:
    # test root: tests
    current_dir_path = os.path.dirname(os.path.abspath(__file__))
    return DirectoryPath(current_dir_path.replace('/', os.sep))
