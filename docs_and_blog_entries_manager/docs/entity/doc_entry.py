from __future__ import annotations

from datetime import datetime
from typing import Optional, List

from common.constants import NON_CATEGORY_GROUP_NAME
from entries.interface import IEntry
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

    def __init__(self, docs_id: str, title: str, dir_path: str, doc_file_name: str, categories: List[str],
                 is_pickup: bool = False, created_at: Optional[datetime] = None, updated_at: Optional[datetime] = None):
        self.__id = docs_id
        self.__title = title
        self.__dir_path = dir_path
        self.__doc_file_name = doc_file_name
        self.__top_category = categories[0] if not len(categories) == 0 else NON_CATEGORY_GROUP_NAME
        self.__categories = categories
        self.__pickup = is_pickup
        self.__created_at: Optional[datetime] = created_at
        self.__updated_at: Optional[datetime] = updated_at

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
    def top_category(self) -> str:
        return self.__top_category

    @property
    def pickup(self) -> bool:
        return self.__pickup

    @property
    def created_at(self) -> str:
        return datetime_functions.convert_to_entry_time_str(self.__created_at)

    @property
    def updated_at(self) -> str:
        return datetime_functions.convert_to_entry_time_str(self.__updated_at)

    @property
    def updated_at_month_day(self):
        return datetime_functions.convert_to_month_day_str(self.__updated_at)

    def convert_id_to_title(self) -> dict[str, str]:
        return {self.id: self.title}

    def convert_md_line(self) -> str:
        return f'- [{self.title}]({self.dir_path}{self.doc_file_name})'

    def serialize(self, json_data=None) -> dict:
        return vars(self)

    @classmethod
    def deserialize(cls, dump_json_data: dict[str, any]) -> DocEntry:
        return DocEntry(
            dump_json_data[DocEntry.FIELD_ID],
            dump_json_data[DocEntry.FIELD_TITLE],
            dump_json_data[DocEntry.FIELD_DIR_PATH],
            dump_json_data[DocEntry.FIELD_DOC_FILE_NAME],
            dump_json_data[DocEntry.FIELD_CATEGORIES],
            # field added later
            dump_json_data[DocEntry.FIELD_PICKUP] if DocEntry.FIELD_PICKUP in dump_json_data else False,
            datetime_functions.convert_entry_time_str_to_datetime(dump_json_data[DocEntry.FIELD_CREATED_AT]),
            datetime_functions.convert_entry_time_str_to_datetime(dump_json_data[DocEntry.FIELD_UPDATED_AT])
        )
