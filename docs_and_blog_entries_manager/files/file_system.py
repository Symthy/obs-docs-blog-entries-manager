import os
from typing import List


def exist_file(target_dir_path: str) -> any:
    return os.path.exists(target_dir_path) and os.path.isfile(target_dir_path)


def exist_dir(target_dir_path: str) -> bool:
    return os.path.exists(target_dir_path) and os.path.isdir(target_dir_path)


def join_path(*paths: str):
    return os.path.join(*paths)


def get_dir_names_in_target_dir(target_dir_path: str) -> List[str]:
    files = os.listdir(target_dir_path)
    return [d for d in files if os.path.isdir(join_path(target_dir_path, d))]


def get_dir_name_from_dir_path(path: str) -> str:
    if path.endswith('/'):
        # dir path: xxx/
        return path[:-1].rsplit('/', 1)[1]
    return path.rsplit('/', 1)[1]
