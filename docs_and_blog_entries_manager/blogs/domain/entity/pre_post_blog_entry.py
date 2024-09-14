from entries.domain.value import CategoryPath, EntryDateTime
from files.value.file_path import FilePath


class PrePostBlogEntry:
    """
    (これからブログに投稿する)投稿前のデータを保持するためのクラス
    """

    def __init__(self, title: str, content: str, category_path: CategoryPath, categories: list[str],
                 doc_image_paths: list[FilePath] = None):
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
    def categories(self) -> list[str]:
        return self.__categories

    @property
    def category_path(self) -> CategoryPath:
        return self.__category_path

    @property
    def updated_at(self) -> EntryDateTime:
        return self.__updated_at

    @property
    def doc_image_paths(self) -> list[FilePath]:
        return self.__doc_image_paths

    @property
    def doc_image_filenames(self) -> list[str]:
        return list(map(lambda path: path.get_file_name_from_file_path(), self.__doc_image_paths))
