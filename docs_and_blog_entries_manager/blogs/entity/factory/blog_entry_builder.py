from typing import List

from blogs.entity.blog_entry import BlogEntry
from blogs.entity.photo.photo_entries import PhotoEntries
from blogs.value.blog_entry_id import BlogEntryId
from entries.values.category_path import CategoryPath
from entries.values.entry_date_time import EntryDateTime


class BlogEntryBuilder:
    def __init__(self, based_blog_entry: BlogEntry = None):
        if based_blog_entry is not None:
            self.__id = based_blog_entry.id
            self.__title = based_blog_entry.title
            self.__page_url = based_blog_entry.page_url
            self.__updated_at = based_blog_entry.updated_at
            self.__category_path = based_blog_entry.category_path
            self.__categories = based_blog_entry.categories
            self.__original_doc_id = based_blog_entry.original_doc_id
            self.__doc_images = based_blog_entry.doc_images

    def id(self, value: BlogEntryId):
        self.__id = value
        return self

    def title(self, value: str):
        self.__title = value
        return self

    def page_url(self, value: str):
        self.__page_url = value
        return self

    def updated_at(self, value: EntryDateTime):
        self.__updated_at = value
        return self

    def category_path(self, value: CategoryPath):
        self.__category_path = value
        return self

    def categories(self, value: List[str]):
        self.__categories = value
        return self

    def original_doc_id(self, value: str):
        self.__original_doc_id = value
        return self

    def doc_images(self, value: PhotoEntries):
        self.__doc_images = value
        return self

    def build(self) -> BlogEntry:
        if self.__id is None:
            raise AttributeError('Invalid blog entry ID')
        # Todo: 他項目のチェック。Validationは entity内に置くべき？
        return BlogEntry(self.__id,
                         self.__title,
                         self.__page_url,
                         self.__updated_at if self.__updated_at is not None else EntryDateTime(),
                         self.__category_path,
                         self.__categories,
                         self.__original_doc_id,
                         self.__doc_images)
