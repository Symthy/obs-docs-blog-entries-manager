from __future__ import annotations

import copy
from datetime import datetime

from blogs.domain.value import BlogContent, BlogEntryId
from entries.domain.value import CategoryPath, EntryDateTime
from .blog_entry import BlogEntry
from .photo_entries import PhotoEntries


class PostedBlogEntry:
    """
    ブログに投稿済みのデータを取得して保持するためのクラス
    """

    def __init__(self, hatena_id: str, entry_id: BlogEntryId, title: str, content: str, page_url: str,
                 last_updated: datetime, categories: list[str], photo_entries: PhotoEntries = PhotoEntries()):
        self.__hatena_id = hatena_id
        updated_at: EntryDateTime = EntryDateTime(last_updated)
        category_path = CategoryPath(categories[0]) if len(categories) >= 1 else CategoryPath.non_category()
        categories = categories[1:] if len(categories) >= 2 else []
        self.__blog_entry = BlogEntry(entry_id, title, page_url, updated_at, category_path, categories, photo_entries)
        self.__photo_entries: PhotoEntries = photo_entries
        self.__content = BlogContent(entry_id, content, category_path, categories, hatena_id)

    @property
    def category_path(self) -> CategoryPath:
        return self.__blog_entry.category_path

    @property
    def title(self) -> str:
        return self.__blog_entry.title

    @property
    def content(self) -> BlogContent:
        return self.__content

    @property
    def photo_entries(self) -> PhotoEntries:
        return self.__photo_entries

    @property
    def updated_at(self) -> EntryDateTime:
        return self.__blog_entry.updated_at

    def blog_entry(self) -> BlogEntry:
        return self.__blog_entry

    def merge_photo_entries(self, images: PhotoEntries) -> PostedBlogEntry:
        new_photo_entries = self.__photo_entries.merge(images)
        cloned_entry = copy.deepcopy(self)
        cloned_entry.__photo_entries = new_photo_entries
        return cloned_entry
