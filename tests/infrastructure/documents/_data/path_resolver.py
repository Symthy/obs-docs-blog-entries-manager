import os


def resolve_test_data_dir_path() -> str:
    current_dir_path = os.path.dirname(os.path.abspath(__file__))
    return current_dir_path.replace('/', os.sep)
