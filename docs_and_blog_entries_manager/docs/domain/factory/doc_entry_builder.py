from typing import Optional

from docs.domain.entity import DocEntry
from docs.domain.value import DocEntryId
from entries.domain.value import CategoryPath, EntryDateTime


class DocEntryBuilder:
    def __init__(self, based_doc_entry: DocEntry = None):
        if based_doc_entry is not None:
            self.__id = based_doc_entry.id
            self.__title = based_doc_entry.title
            self.__doc_file_name = based_doc_entry.doc_file_name
            self.__category_path = based_doc_entry.category_path
            self.__categories = based_doc_entry.categories
            self.__pickup = based_doc_entry.pickup
            self.__created_at: Optional[EntryDateTime] = based_doc_entry.created_at
            self.__updated_at: Optional[EntryDateTime] = based_doc_entry.updated_at

    def id(self, value: DocEntryId):
        self.__id = value
        return self

    def title(self, value: str):
        self.__title = value
        return self

    def doc_file_name(self, value: str):
        self.__doc_file_name = value
        return self

    def category_path(self, value: CategoryPath):
        self.__category_path = value
        return self

    def categories(self, *values: str):
        self.__categories = list(set(values))
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
        if not ((self.__id is None and self.__created_at is None) or (
                self.__id is not None and self.__created_at is not None)):
            raise AttributeError(f'Invalid id and created_at (id: {self.__id}, created_at: {self.__created_at})')
        # Todo: 他項目のチェック。Validationは entity内に置くべき？
        current_date_time = EntryDateTime()
        return DocEntry(
            self.__id if self.__id is not None else DocEntryId.build(current_date_time),
            self.__title,
            self.__doc_file_name,
            self.__category_path,
            self.__categories,
            self.__pickup,
            self.__created_at if self.__created_at is not None else current_date_time,
            self.__updated_at if self.__updated_at is not None else current_date_time
        )
