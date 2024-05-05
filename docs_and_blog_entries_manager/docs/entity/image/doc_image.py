from entries.values.entry_date_time import EntryDateTime
from files import file_system, image_file


class DocImage:
    def __init__(self, doc_entry_dir_path: str, file_name: str, image_data: bytes,
                 created_at: EntryDateTime = EntryDateTime(), updated_at: EntryDateTime = EntryDateTime()):
        self.__doc_entry_dir_path: str = file_system.join_path(doc_entry_dir_path, 'images')
        self.__file_name: str = file_name
        self.__image_data: bytes = image_data
        self.__created_at = created_at
        self.__updated_at = updated_at

    @property
    def file_path(self) -> str:
        return file_system.join_path(self.__doc_entry_dir_path, self.__file_name)

    @property
    def image_data(self) -> bytes:
        return self.__image_data

    @property
    def image_base64(self) -> str:
        return image_file.encode_base64(self.__image_data)

    @property
    def created_at(self) -> EntryDateTime:
        return self.__created_at

    @property
    def updated_at(self) -> EntryDateTime:
        return self.__updated_at
