from typing import List

from domain.entries.values.category_path import CategoryPath
from domain.entries.values.entry_date_time import EntryDateTime


class PostBlogEntry:
    """
    これからブログに登録するデータを保持するためのクラス
    """

    def __init__(self, title: str, content: str, category_path: CategoryPath, categories: List[str],
                 doc_image_paths: List[str] = None):
        self.__title = title
        self.__content = content
        self.__category_path = category_path
        self.__categories = categories
        self.__updated_at = EntryDateTime()
        self.__doc_image_paths = doc_image_paths if doc_image_paths is not None else []

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
    def category_path(self) -> CategoryPath:
        return self.__category_path

    @property
    def updated_at(self) -> EntryDateTime:
        return self.__updated_at

    @property
    def doc_image_paths(self) -> List[str]:
        return self.__doc_image_paths
