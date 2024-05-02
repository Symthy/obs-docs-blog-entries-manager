from __future__ import annotations

from datetime import datetime
from typing import List, Optional, Dict

from docs_and_blog_entries_manager.blogs.entity.photo.photo_entries import PhotoEntries
from docs_and_blog_entries_manager.common.constants import NON_CATEGORY_GROUP_NAME
from docs_and_blog_entries_manager.entries.interface import IEntry
from docs_and_blog_entries_manager.ltimes import datetime_functions


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

    def __init__(self, entry_id: str, title: str, content: str, page_url: str, last_updated: Optional[datetime],
                 categories: List[str], doc_id: Optional[str] = None, doc_images: PhotoEntries = PhotoEntries()):
        self.__id = entry_id
        self.__title = title
        self.__content = content  # No dump
        self.__page_url = page_url
        self.__updated_at: Optional[datetime] = last_updated  # Make it optional just in case
        self.__top_category = categories[0] if not len(categories) == 0 else NON_CATEGORY_GROUP_NAME
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
    def content(self):
        return self.__content

    @property
    def page_url(self):
        return self.__page_url

    @property
    def updated_at(self) -> str:
        return datetime_functions.convert_to_entry_time_str(self.__updated_at)

    @property
    def updated_at_month_day(self) -> str:
        return datetime_functions.convert_to_month_day_str(self.__updated_at)

    @property
    def categories(self) -> List[str]:
        return self.__categories

    @property
    def top_category(self) -> str:
        return self.__top_category

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

    def add_photo_entries(self, photo_entries: Optional[PhotoEntries] = None):
        if photo_entries is None:
            return
        self.__doc_images.merge(photo_entries)

    def convert_id_to_title(self) -> Dict[str, str]:
        return {self.id: self.title}

    def convert_md_line(self) -> str:
        return f'- [{self.title}]({self.page_url}) ({self.updated_at_month_day})'

    def serialize(self) -> object:
        return vars(self)

    @classmethod
    def deserialize(cls, dump_data: Dict[str, any]) -> BlogEntry:
        return BlogEntry(
            dump_data[BlogEntry.FIELD_ID],
            dump_data[BlogEntry.FIELD_TITLE],
            '',  # content is not dump
            dump_data[BlogEntry.FIELD_PAGE_URL],
            datetime_functions.convert_entry_time_str_to_datetime(dump_data[BlogEntry.FIELD_UPDATED_AT]),
            dump_data[BlogEntry.FIELD_CATEGORIES],
            dump_data[BlogEntry.FIELD_ORIGINAL_DOC_ID],
            PhotoEntries.deserialize(dump_data[BlogEntry.FIELD_DOC_IMAGES])
        )
