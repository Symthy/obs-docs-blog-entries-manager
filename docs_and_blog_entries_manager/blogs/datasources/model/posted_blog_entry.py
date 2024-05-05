from __future__ import annotations

from datetime import datetime
from typing import Optional, List

from blogs.entity.blog_entry import BlogEntry
from blogs.entity.photo.photo_entries import PhotoEntries
from blogs.value.blog_content import BlogContent
from blogs.value.blog_entry_id import BlogEntryId
from common.constants import NON_CATEGORY_NAME
from entries.values.category_path import CategoryPath
from entries.values.entry_date_time import EntryDateTime


class PostedBlogEntry:
    """
    ブログに投稿済みのデータを取得して保持するためのクラス
    """

    def __init__(self, hatena_id: str, entry_id: str, title: str, content: str, page_url: str, last_updated: datetime,
                 categories: List[str], doc_id: Optional[str] = None,
                 images: PhotoEntries = PhotoEntries()):
        self.__hatena_id = hatena_id
        self.__id = entry_id
        self.__title = title
        self.__page_url = page_url
        self.__updated_at: EntryDateTime = EntryDateTime(last_updated)
        top_category = categories[0] if len(categories) >= 1 else NON_CATEGORY_NAME
        self.__category_path = CategoryPath(top_category)
        self.__categories = categories if len(categories) >= 2 else []
        self.__original_doc_id = doc_id
        self.__images: PhotoEntries = images
        self.__content = BlogContent(content, self.__category_path, self.__categories, hatena_id)

    @property
    def category_path(self) -> CategoryPath:
        return self.__category_path

    @property
    def content(self) -> BlogContent:
        return self.__content

    def convert_to_blog_entry(self) -> BlogEntry:
        return BlogEntry(BlogEntryId(self.__id), self.__title, self.__page_url, self.__updated_at,
                         self.__category_path, self.__categories, self.__original_doc_id, self.__images)

    def merge_photo_entries(self, images: PhotoEntries) -> PostedBlogEntry:
        new_photo_entries = self.__images.merge(images)
        return PostedBlogEntry(self.__hatena_id, self.__id, self.__title, self.__content.value, self.__page_url,
                               self.__updated_at.to_datetime(), [self.__category_path.value, self.__categories],
                               self.__original_doc_id, new_photo_entries)
