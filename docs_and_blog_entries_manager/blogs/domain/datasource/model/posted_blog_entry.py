from __future__ import annotations

from datetime import datetime

from blogs.domain.entity import BlogEntry
from blogs.domain.entity import PhotoEntries
from blogs.domain.value import BlogContent
from blogs.domain.value import BlogEntryId
from entries.domain.value import CategoryPath
from entries.domain.value import EntryDateTime


class PostedBlogEntry:
    """
    ブログに投稿済みのデータを取得して保持するためのクラス
    """

    def __init__(self, hatena_id: str, entry_id: BlogEntryId, title: str, content: str, page_url: str,
                 last_updated: datetime, categories: list[str], photo_entries: PhotoEntries = PhotoEntries()):
        self.__hatena_id = hatena_id
        self.__id = entry_id
        self.__title = title
        self.__page_url = page_url
        self.__updated_at: EntryDateTime = EntryDateTime(last_updated)
        self.__category_path = CategoryPath(categories[0]) if len(categories) >= 1 else CategoryPath.non_category()
        self.__categories = categories[1:] if len(categories) >= 2 else []
        self.__photo_entries: PhotoEntries = photo_entries
        self.__content = BlogContent(entry_id, content, self.__category_path, self.__categories, hatena_id)

    @property
    def category_path(self) -> CategoryPath:
        return self.__category_path

    @property
    def title(self) -> str:
        return self.__title

    @property
    def content(self) -> BlogContent:
        return self.__content

    @property
    def photo_entries(self) -> PhotoEntries:
        return self.__photo_entries

    @property
    def updated_at(self) -> EntryDateTime:
        return self.__updated_at

    def convert_to_blog_entry(self) -> BlogEntry:
        return BlogEntry(self.__id, self.__title, self.__page_url, self.__updated_at,
                         self.__category_path, self.__categories, self.__photo_entries)

    def merge_photo_entries(self, images: PhotoEntries) -> PostedBlogEntry:
        new_photo_entries = self.__photo_entries.merge(images)
        return PostedBlogEntry(self.__hatena_id, self.__id, self.__title, self.__content.value, self.__page_url,
                               self.__updated_at.to_datetime(), [self.__category_path.value.value, self.__categories],
                               new_photo_entries)
