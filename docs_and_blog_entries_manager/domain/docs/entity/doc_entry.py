from __future__ import annotations

from typing import List

from common.constants import BLOG_CATEGORY
from domain.docs.value.doc_entry_id import DocEntryId
from domain.entries.interface import IEntry
from domain.entries.values.category_path import CategoryPath
from domain.entries.values.entry_date_time import EntryDateTime
from files import file_system


class DocEntry(IEntry):
    FIELD_ID = 'id'
    FIELD_TITLE = 'title'
    FIELD_DOC_FILE_NAME = 'doc_file_name'
    FIELD_CATEGORY_PATH = 'category_path'
    FIELD_CATEGORIES = 'categories'
    FIELD_PICKUP = 'pickup'
    FIELD_CREATED_AT = 'created_at'
    FIELD_UPDATED_AT = 'updated_at'

    def __init__(self, doc_id: DocEntryId, title: str, doc_file_name: str, category_path: CategoryPath,
                 categories: List[str], is_pickup: bool = False, created_at: EntryDateTime = None,
                 updated_at: EntryDateTime = None):
        self.__id = doc_id
        self.__title = title
        self.__doc_file_name = doc_file_name
        self.__category_path = category_path
        self.__categories = categories
        self.__pickup = is_pickup
        self.__created_at = created_at if created_at is not None else EntryDateTime()
        self.__updated_at = updated_at if updated_at is not None else self.__created_at

    @property
    def id(self) -> DocEntryId:
        return self.__id

    @property
    def title(self) -> str:
        return self.__title

    @property
    def doc_file_path(self) -> str:
        return file_system.join_path('.', self.category_path.value, self.__doc_file_name)

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
    def created_at(self) -> EntryDateTime:
        return self.__created_at

    @property
    def updated_at(self) -> EntryDateTime:
        return self.__updated_at

    @property
    def updated_at_month_day(self):
        return self.__updated_at.to_month_day_str()

    @property
    def is_inprogress(self) -> bool:
        return self.__category_path.is_empty

    @property
    def is_completed(self) -> bool:
        return not self.is_inprogress

    def equals_path(self, other: DocEntry) -> bool:
        return self.category_path == other.category_path

    def contains_blog_category(self) -> bool:
        return BLOG_CATEGORY in self.__categories

    def convert_id_to_title(self) -> dict[DocEntryId, str]:
        return {self.id: self.title}

    def update_category(self, category: str) -> DocEntry:
        return DocEntry(self.__id, self.__title, self.__doc_file_name, self.__category_path,
                        [*self.__categories, category], self.__pickup, self.__created_at, self.__updated_at)

    def convert_md_line(self) -> str:
        blog_mark = '【B】' if self.contains_blog_category else ''
        return f'- {blog_mark}[{self.title}]({self.doc_file_path}) (ID:{self.id})'

    def serialize(self) -> dict:
        return vars(self)
