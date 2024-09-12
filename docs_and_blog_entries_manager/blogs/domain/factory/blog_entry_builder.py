from typing import List

from blogs.domain.entity import BlogEntry
from blogs.domain.entity import PhotoEntries
from blogs.domain.value import BlogEntryId
from entries.domain.value import CategoryPath
from entries.domain.value import EntryDateTime


class BlogEntryBuilder:
    def __init__(self, based_blog_entry: BlogEntry = None):
        if based_blog_entry is not None:
            self.__id = based_blog_entry.id
            self.__title = based_blog_entry.title
            self.__page_url = based_blog_entry.page_url
            self.__updated_at = based_blog_entry.updated_at
            self.__category_path = based_blog_entry.category_path
            self.__categories = based_blog_entry.categories
            self.__images = based_blog_entry.images
            self.__pickup = based_blog_entry.pickup

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

    def images(self, value: PhotoEntries):
        self.__images = value
        return self

    def pickup(self, value: bool):
        self.__pickup = value

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
                         self.__images,
                         self.__pickup if self.__pickup is not None else False)
