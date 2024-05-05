from typing import Optional, List

from docs.entity.doc_entry import DocEntry
from docs.entity.factory.doc_entry_id_builder import DocEntryIdBuilder
from entries.values.category_path import CategoryPath
from entries.values.entry_date_time import EntryDateTime


class DocEntryBuilder:
    def __init__(self, doc_entry_id_builder: DocEntryIdBuilder, based_doc_entry: DocEntry = None):
        self.__doc_entry_id_builder = doc_entry_id_builder
        if based_doc_entry is not None:
            self.__id = based_doc_entry.id
            self.__title = based_doc_entry.title
            self.__dir_path = based_doc_entry.dir_path
            self.__doc_file_name = based_doc_entry.doc_file_name
            self.__category_path = based_doc_entry.category_path
            self.__categories = based_doc_entry.categories
            self.__pickup = based_doc_entry.pickup
            self.__created_at: Optional[EntryDateTime] = based_doc_entry.created_at
            self.__updated_at: Optional[EntryDateTime] = based_doc_entry.updated_at

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

    def category_path(self, value: CategoryPath):
        self.__category_path = value
        return self

    def categories(self, value: List[str]):
        self.__categories = value
        return self

    def pickup(self, value: bool):
        self.__pickup = value
        return self

    def created_at(self, value: EntryDateTime):
        self.__created_at = value
        return self

    def updated_at(self, value: EntryDateTime):
        self.__updated_at = value
        return self

    def build(self):
        current_date_time = EntryDateTime()
        return DocEntry(
            self.__id if self.__id is not None else self.__doc_entry_id_builder.build(current_date_time),
            self.__title,
            self.__dir_path,
            self.__doc_file_name,
            self.__category_path,
            self.__categories,
            self.__pickup,
            self.__created_at if self.__created_at is not None else current_date_time,
            self.__updated_at if self.__created_at is not None else current_date_time
        )
