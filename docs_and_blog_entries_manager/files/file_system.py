import os


def exist_file(target_dir_path: str):
    return os.path.exists(target_dir_path) and os.path.isfile(target_dir_path)


def exist_dir(target_dir_path: str) -> bool:
    return os.path.exists(target_dir_path) and os.path.isdir(target_dir_path)
