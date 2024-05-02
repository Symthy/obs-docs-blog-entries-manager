from datetime import datetime
from typing import Optional, List

from docs.entity.doc_entry import DocEntry
from ltimes import datetime_functions


class DocEntryBuilder:
    def __init__(self, based_doc_entry: DocEntry = None):
        if based_doc_entry is not None:
            self.__id = based_doc_entry.id
            self.__title = based_doc_entry.title
            self.__dir_path = based_doc_entry.dir_path
            self.__doc_file_name = based_doc_entry.doc_file_name
            self.__categories = based_doc_entry.categories
            self.__pickup = based_doc_entry.pickup
            self.__created_at: Optional[datetime] = datetime_functions.convert_entry_time_str_to_datetime(
                based_doc_entry.created_at)
            self.__updated_at: Optional[datetime] = datetime_functions.convert_entry_time_str_to_datetime(
                based_doc_entry.updated_at)

    def id(self, value: str):
        self.__id = value
        return self

    def title(self, value: str):
        self.__title = value
        return self

    def dir_path(self, value: str):
        self.__dir_path = value
        return self

    def doc_file_name(self, value: str):
        self.__doc_file_name = value
        return self

    def categories(self, value: List[str]):
        self.__categories = value
        return self

    def pickup(self, value: bool):
        self.__pickup = value
        return self

    def created_at(self, value: datetime):
        self.__created_at = value
        return self

    def updated_at(self, value: datetime):
        self.__updated_at = value
        return self

    def build(self):
        return DocEntry(
            self.__id,
            self.__title,
            self.__dir_path,
            self.__doc_file_name,
            self.__categories,
            self.__pickup,
            self.__created_at if self.__created_at is not None else datetime_functions.current_datetime(),
            self.__updated_at if self.__created_at is not None else datetime_functions.current_datetime()
        )
