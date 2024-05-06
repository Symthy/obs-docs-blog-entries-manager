from __future__ import annotations

from typing import List, Optional, Dict

from domain.blogs.entity.photo.photo_entries import PhotoEntries
from domain.blogs.value.blog_entry_id import BlogEntryId
from domain.entries.interface import IEntry
from domain.entries.values.category_path import CategoryPath
from domain.entries.values.entry_date_time import EntryDateTime


class BlogEntry(IEntry):
    FIELD_ID = 'id'
    FIELD_TITLE = 'title'
    FIELD_CONTENT = 'content'
    FIELD_PAGE_URL = 'page_url'
    FIELD_CATEGORY_PATH = 'category_path'
    FIELD_CATEGORIES = 'categories'
    FIELD_UPDATED_AT = 'updated_at'
    FIELD_ORIGINAL_DOC_ID = 'original_doc_id'
    FIELD_DOC_IMAGES = 'doc_images'

    def __init__(self, entry_id: BlogEntryId, title: str, page_url: str, last_updated: EntryDateTime,
                 category_path: CategoryPath, categories: List[str], images: PhotoEntries = PhotoEntries()):
        self.__id = entry_id
        self.__title = title
        self.__page_url = page_url
        self.__updated_at: EntryDateTime = last_updated
        self.__category_path = category_path
        self.__categories = categories
        self.__images: PhotoEntries = images

    @property
    def id(self) -> BlogEntryId:
        return self.__id

    @property
    def title(self):
        return self.__title

    @property
    def page_url(self):
        return self.__page_url

    @property
    def updated_at(self) -> EntryDateTime:
        return self.__updated_at

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
    def images(self) -> Optional[PhotoEntries]:
        return self.__images if not self.is_images_empty() else None

    def is_images_empty(self) -> bool:
        return self.__images.is_empty()

    def convert_id_to_title(self) -> Dict[BlogEntryId, str]:
        return {self.id: self.title}

    def convert_md_line(self) -> str:
        return f'- [{self.title}]({self.page_url}) ({self.updated_at_month_day})'

    def serialize(self) -> object:
        return vars(self)

    @classmethod
    def deserialize(cls, json_data: Dict[str, any]) -> BlogEntry:
        return BlogEntry(
            BlogEntryId(json_data[BlogEntry.FIELD_ID]),
            json_data[BlogEntry.FIELD_TITLE],
            json_data[BlogEntry.FIELD_PAGE_URL],
            EntryDateTime(json_data[BlogEntry.FIELD_UPDATED_AT]),
            CategoryPath(json_data[BlogEntry.FIELD_CATEGORY_PATH]),
            json_data[BlogEntry.FIELD_CATEGORIES],
            json_data[BlogEntry.FIELD_ORIGINAL_DOC_ID],
            PhotoEntries.deserialize(json_data[BlogEntry.FIELD_DOC_IMAGES])
        )
