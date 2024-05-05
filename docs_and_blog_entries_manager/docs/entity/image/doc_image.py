from datetime import datetime

from files import file_system, image_file


class DocImage:
    def __init__(self, dir_path: str, file_name: str, image_data: bytes, created_at: datetime, updated_at: datetime):
        self.__dir_path: str = dir_path
        self.__file_name: str = file_name
        self.__image_data: bytes = image_data
        self.__created_at: datetime = created_at
        self.__updated_at: datetime = updated_at

    @property
    def file_path(self) -> str:
        return file_system.join_path(self.__dir_path, self.__file_name)

    @property
    def image_data(self) -> bytes:
        return self.__image_data

    @property
    def image_base64(self) -> str:
        return image_file.encode_base64(self.__image_data)

    @property
    def created_at(self) -> datetime:
        return self.__created_at

    @property
    def updated_at(self) -> datetime:
        return self.__updated_at
