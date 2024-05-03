from __future__ import annotations

from datetime import datetime
from typing import List

from entries.interface import IEntry
from entries.values.category_path import CategoryPath
from entries.values.entry_time import EntryDateTime
from ltimes import datetime_functions


class DocEntry(IEntry):
    FIELD_ID = 'id'
    FIELD_TITLE = 'title'
    FIELD_DIR_PATH = 'dir_path'
    FIELD_DOC_FILE_NAME = 'doc_file_name'
    FIELD_TOP_CATEGORY = 'top_category'
    FIELD_CATEGORIES = 'categories'
    FIELD_PICKUP = 'pickup'
    FIELD_CREATED_AT = 'created_at'
    FIELD_UPDATED_AT = 'updated_at'

    def __init__(self, docs_id: str, title: str, dir_path: str, doc_file_name: str, category_path: CategoryPath,
                 categories: List[str], is_pickup: bool = False, created_at: datetime = None,
                 updated_at: datetime = None):
        self.__id = docs_id
        self.__title = title
        self.__dir_path = dir_path
        self.__doc_file_name = doc_file_name
        self.__category_path = category_path
        self.__categories = categories
        self.__pickup = is_pickup
        self.__created_at = EntryDateTime(created_at) if created_at is not None else EntryDateTime()
        self.__updated_at = EntryDateTime(updated_at) if updated_at is not None else self.__created_at

    @property
    def id(self) -> str:
        return self.__id

    @property
    def title(self) -> str:
        return self.__title

    @property
    def dir_path(self) -> str:
        return self.__dir_path

    @property
    def doc_file_name(self) -> str:
        return self.__doc_file_name

    @property
    def categories(self) -> List[str]:
        return self.__categories

    @property
    def category_path(self) -> CategoryPath:
        return self.__category_path

    @property
    def pickup(self) -> bool:
        return self.__pickup

    @property
    def created_at(self) -> str:
        return self.__created_at.to_str()

    @property
    def updated_at(self) -> str:
        return self.__updated_at.to_str()

    @property
    def updated_at_month_day(self):
        return self.__updated_at.to_month_day_str()

    def convert_id_to_title(self) -> dict[str, str]:
        return {self.id: self.title}

    def convert_md_line(self) -> str:
        return f'- [{self.title}]({self.dir_path}{self.doc_file_name})'

    def serialize(self, json_data=None) -> dict:
        return vars(self)

    @classmethod
    def deserialize(cls, json_data: dict[str, any]) -> DocEntry:
        return DocEntry(
            json_data[DocEntry.FIELD_ID],
            json_data[DocEntry.FIELD_TITLE],
            json_data[DocEntry.FIELD_DIR_PATH],
            json_data[DocEntry.FIELD_DOC_FILE_NAME],
            json_data[DocEntry.FIELD_CATEGORIES],
            # field added later
            json_data[DocEntry.FIELD_PICKUP] if DocEntry.FIELD_PICKUP in json_data else False,
            datetime_functions.convert_entry_time_str_to_datetime(json_data[DocEntry.FIELD_CREATED_AT]),
            datetime_functions.convert_entry_time_str_to_datetime(json_data[DocEntry.FIELD_UPDATED_AT])
        )
