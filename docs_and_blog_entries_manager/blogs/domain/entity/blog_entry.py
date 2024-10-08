from __future__ import annotations

from typing import List, Optional

from blogs.domain.value.blog_entry_id import BlogEntryId
from entries.domain.interface import IEntry
from entries.domain.value import CategoryPath, EntryDateTime
from entries.domain.value.entry_type import EntryType
from .photo_entries import PhotoEntries


class BlogEntry(IEntry):
    FIELD_ID = 'id'
    FIELD_TITLE = 'title'
    FIELD_CONTENT = 'content'
    FIELD_PAGE_URL = 'page_url'
    FIELD_PICKUP = 'pickup'
    FIELD_CATEGORY_PATH = 'category_path'
    FIELD_CATEGORIES = 'categories'
    FIELD_UPDATED_AT = 'updated_at'
    FIELD_IMAGES = 'images'

    def __init__(self, entry_id: BlogEntryId, title: str, page_url: str, last_updated: EntryDateTime,
                 category_path: CategoryPath, categories: List[str], images: PhotoEntries = PhotoEntries(),
                 pickup: bool = False):
        self.__id = entry_id
        self.__title = title
        self.__page_url = page_url
        self.__updated_at: EntryDateTime = last_updated
        self.__category_path = category_path
        self.__categories = categories
        self.__pickup = pickup
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
    def pickup(self) -> bool:
        return self.__pickup

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
        return self.__images if not self.__images.is_empty() else None

    @property
    def entry_type(self) -> EntryType:
        return EntryType.BLOG

    def update_pickup(self, pickup: bool) -> BlogEntry:
        return BlogEntry(self.id, self.title, self.page_url, self.updated_at, self.category_path, self.categories,
                         self.images, pickup)

    def convert_md_line(self) -> str:
        return f'- [{self.title}]({self.page_url}) ({self.updated_at_month_day})'

    def serialize(self) -> object:
        return vars(self)
