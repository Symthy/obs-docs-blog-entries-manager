from typing import List, Optional

from blogs.entity.photo.photo_entries import PhotoEntries
from common.constants import NON_CATEGORY_GROUP_NAME
from ltimes import datetime_functions


class PostBlogEntry:

    def __init__(self, entry_id: str, title: str, content: str, categories: List[str],
                 doc_images: PhotoEntries = PhotoEntries()):
        self.__id = entry_id
        self.__title = title
        self.__content = content  # No dump
        self.__top_category = categories[0] if not len(categories) == 0 else NON_CATEGORY_GROUP_NAME
        self.__categories = categories
        self.__updated_at = datetime_functions.resolve_entry_current_time()
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
    def categories(self) -> List[str]:
        return self.__categories

    @property
    def top_category(self) -> str:
        return self.__top_category

    @property
    def updated_at(self) -> str:
        return self.__updated_at

    @property
    def doc_images(self) -> Optional[PhotoEntries]:
        if self.is_images_empty():
            return None
        return self.__doc_images

    def is_images_empty(self) -> bool:
        return self.__doc_images.is_empty()
