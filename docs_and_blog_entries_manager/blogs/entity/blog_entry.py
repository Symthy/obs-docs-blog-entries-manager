from __future__ import annotations

from datetime import datetime
from typing import List, Optional, Dict

from docs_and_blog_entries_manager.blogs.entity.photo.photo_entries import PhotoEntries
from docs_and_blog_entries_manager.entries.interface import IEntry
from docs_and_blog_entries_manager.ltimes import datetime_functions
from entries.values.category_path import CategoryPath
from entries.values.entry_time import EntryDateTime


class BlogEntry(IEntry):
    FIELD_ID = 'id'
    FIELD_TITLE = 'title'
    FIELD_CONTENT = 'content'
    FIELD_PAGE_URL = 'page_url'
    FIELD_TOP_CATEGORY = 'top_category'
    FIELD_CATEGORIES = 'categories'
    FIELD_UPDATED_AT = 'updated_at'
    FIELD_ORIGINAL_DOC_ID = 'original_doc_id'
    FIELD_DOC_IMAGES = 'doc_images'

    def __init__(self, entry_id: str, title: str, page_url: str, last_updated: datetime, category_path: str,
                 categories: List[str], doc_id: Optional[str] = None, doc_images: PhotoEntries = PhotoEntries()):
        self.__id = entry_id
        self.__title = title
        self.__page_url = page_url
        self.__updated_at: EntryDateTime = EntryDateTime(last_updated)
        self.__category_path = CategoryPath(category_path)
        self.__categories = categories
        self.__original_doc_id = doc_id
        self.__doc_images: PhotoEntries = doc_images

    @property
    def id(self):
        return self.__id

    @property
    def title(self):
        return self.__title

    @property
    def page_url(self):
        return self.__page_url

    @property
    def updated_at(self) -> str:
        return self.__updated_at.to_str()

    @property
    def updated_at_month_day(self) -> str:
        return self.__updated_at.to_month_day_str()

    @property
    def categories(self) -> List[str]:
        return self.__categories

    @property
    def category_path(self) -> CategoryPath:
        return self.__category_path

    @property
    def original_doc_id(self):
        return self.__original_doc_id

    @property
    def doc_images(self) -> Optional[PhotoEntries]:
        if self.is_images_empty():
            return None
        return self.__doc_images

    def is_images_empty(self) -> bool:
        return self.__doc_images.is_empty()

    def convert_id_to_title(self) -> Dict[str, str]:
        return {self.id: self.title}

    def convert_md_line(self) -> str:
        return f'- [{self.title}]({self.page_url}) ({self.updated_at_month_day})'

    def serialize(self) -> object:
        return vars(self)

    @classmethod
    def deserialize(cls, json_data: Dict[str, any]) -> BlogEntry:
        return BlogEntry(
            json_data[BlogEntry.FIELD_ID],
            json_data[BlogEntry.FIELD_TITLE],
            json_data[BlogEntry.FIELD_PAGE_URL],
            datetime_functions.convert_entry_time_str_to_datetime(json_data[BlogEntry.FIELD_UPDATED_AT]),
            json_data[BlogEntry.FIELD_CATEGORIES],
            json_data[BlogEntry.FIELD_ORIGINAL_DOC_ID],
            PhotoEntries.deserialize(json_data[BlogEntry.FIELD_DOC_IMAGES])
        )
