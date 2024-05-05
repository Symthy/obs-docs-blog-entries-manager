from __future__ import annotations

from datetime import datetime
from typing import Optional, List

from blogs.entity.blog_entry import BlogEntry
from blogs.entity.photo.photo_entries import PhotoEntries
from entries.values.category_path import CategoryPath
from entries.values.entry_date_time import EntryDateTime


class PostedBlogEntry:
    """
    ブログに投稿済みのデータを取得して保持するためのクラス
    """

    def __init__(self, entry_id: str, title: str, content: str, page_url: str, last_updated: datetime,
                 category_path: str, categories: List[str], doc_id: Optional[str] = None,
                 images: PhotoEntries = PhotoEntries()):
        self.__id = entry_id
        self.__title = title
        self.__page_url = page_url
        self.__updated_at: EntryDateTime = EntryDateTime(last_updated)
        self.__category_path = CategoryPath(category_path)
        self.__categories = categories
        self.__original_doc_id = doc_id
        self.__images: PhotoEntries = images
        self.__content = content

    @property
    def content(self) -> str:
        return self.__content

    def convert_to_blog_entry(self) -> BlogEntry:
        return BlogEntry(self.__id, self.__title, self.__page_url, EntryDateTime(self.__updated_at.to_datetime()),
                         self.__category_path.value, self.__categories, self.__original_doc_id, self.__images)

    def merge_photo_entries(self, images: PhotoEntries) -> PostedBlogEntry:
        new_photo_entries = self.__images.merge(images)
        return PostedBlogEntry(self.__id, self.__title, self.__content, self.__page_url,
                               self.__updated_at.to_datetime(), self.__category_path.value, self.__categories,
                               self.__original_doc_id, new_photo_entries)
