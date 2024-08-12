from __future__ import annotations

import os
import shutil
from datetime import datetime
from pathlib import Path


class DirectoryPath:
    def __init__(self, *dir_path: str):
        self.__dir_path = '/'.join(dir_path)

    @property
    def value(self) -> str:
        return self.__dir_path

    def exist(self) -> bool:
        return os.path.exists(self.__dir_path) and os.path.isdir(self.__dir_path)

    def get_file_paths_in_target_dir(self) -> list[FilePath]:
        files = os.listdir(self.__dir_path)
        return [FilePath(self.__dir_path + f) for f in files if os.path.isfile(os.path.join(self.__dir_path, f))]

    def get_dir_name_from_dir_path(self) -> str:
        if self.__dir_path.endswith('/'):
            # dir path: xxx/
            return self.__dir_path[:-1].rsplit('/', 1)[1]
        return self.__dir_path.rsplit('/', 1)[1]

    def join(self, dir_path: DirectoryPath) -> DirectoryPath:
        return DirectoryPath(self.__dir_path, dir_path.value)

    def join_file_path(self, file_path: FilePath):
        return FilePath(self.__dir_path, file_path.value)

    def add_dir(self, dir_name: str) -> DirectoryPath:
        return DirectoryPath(self.__dir_path, dir_name)

    def add_file(self, file_name: str) -> FilePath:
        return FilePath(self.__dir_path, file_name)

    def __str__(self):
        print(self.__dir_path)
        return self.__dir_path

    def __eq__(self, other: DirectoryPath):
        return self.__dir_path == other.__dir_path


class FilePath:
    # ファイルパスは実行環境が Linux のため、基本的にLinux統一になる
    def __init__(self, *file_path: str):
        self.__file_path = '/'.join(file_path)

    @property
    def value(self) -> str:
        return self.__file_path

    def exist(self) -> bool:
        return os.path.exists(self.__file_path) and os.path.isfile(self.__file_path)

    def get_file_name(self) -> str:
        return os.path.basename(self.__file_path).replace('\\', '/')

    def get_file_name_without_ext(self) -> str:
        return os.path.splitext(os.path.basename(self.__file_path))[0]

    def get_file_extension(self) -> str:
        split_str = self.__file_path.rsplit('.', 1)
        extension = split_str[-1].lower()
        return extension

    def get_dir_path_from_file_path(self) -> DirectoryPath:
        return DirectoryPath(self.__file_path.rsplit('/', 1)[0])

    def get_created_file_time(self) -> datetime:
        created_unix_time = Path(self.__file_path).stat().st_ctime
        created_date_time = datetime.fromtimestamp(created_unix_time)
        return created_date_time

    def get_updated_file_time(self) -> datetime:
        return datetime.fromtimestamp(os.path.getmtime(self.__file_path))

    def copy_file(self, to_path: FilePath):
        shutil.copy2(self.__file_path, to_path.value)

    def remove_file(self):
        os.remove(self.__file_path)

    def __str__(self):
        return self.__file_path

    def __eq__(self, other: FilePath):
        return self.__file_path == other.__file_path
