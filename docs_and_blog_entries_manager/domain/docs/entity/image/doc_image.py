from domain.entries.values.entry_date_time import EntryDateTime
from files import image_file
from files.value.file_path import FilePath, DirectoryPath


class DocImage:
    def __init__(self, doc_entry_dir_path: DirectoryPath, file_name: str, image_data: bytes,
                 created_at: EntryDateTime = EntryDateTime(), updated_at: EntryDateTime = EntryDateTime()):
        self.__image_dir_path: DirectoryPath = doc_entry_dir_path.add_dir('images')
        self.__file_name: str = file_name
        self.__image_data: bytes = image_data
        self.__created_at = created_at
        self.__updated_at = updated_at

    @property
    def file_path(self) -> FilePath:
        return self.__image_dir_path.add_file(self.__file_name)

    @property
    def file_link(self) -> str:
        return f'![]({self.file_path})'

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
