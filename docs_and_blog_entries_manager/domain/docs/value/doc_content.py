import re
from typing import List

from common.constants import NON_CATEGORY_NAME
from domain.entries.values.category_path import CategoryPath
from files import file_system


class DocContent:
    __DOCUMENT_IMAGE_LINK_REGEX = r'!\[.*\]\((.+)\)'
    __DOCUMENT_CATEGORY_REGEX = r'#(\S+)'

    def __init__(self, content: str, doc_entry_dir_path: str):
        self.__content = content
        self.__image_paths = self.__extract_image_paths(doc_entry_dir_path)
        all_categories = self.__extract_categories()
        self.__categories = all_categories[1:] if len(all_categories) >= 2 else []
        self.__category_path = self.__categories[0] if len(all_categories) >= 1 else NON_CATEGORY_NAME

    def __extract_image_paths(self, doc_dir_path: str) -> List[str]:
        # 画像ファイルのパスはmdファイルからの相対パス (image/xxxx)
        image_paths = re.findall(self.__DOCUMENT_IMAGE_LINK_REGEX, self.__content)
        return list(map(lambda path: file_system.join_path(doc_dir_path, path), image_paths))

    def __extract_categories(self) -> List[str]:
        categories = re.findall(self.__DOCUMENT_CATEGORY_REGEX, self.__content)
        return categories

    @property
    def value(self) -> str:
        return self.__content

    @property
    def value_with_removed_categories(self):
        # BlogContent変換用。タグが付いている行は削除する。はてブ上ではタグはセクションとして扱われてしまう
        content = re.sub(r'^[ \t]*#\S+[[ \t]+#\S+]*(\r\n|\n)$', '', self.__content, flags=re.MULTILINE)
        return content

    @property
    def image_paths(self) -> List[str]:
        return self.__image_paths

    @property
    def category_path(self) -> CategoryPath:
        return self.__category_path

    @property
    def categories(self) -> List[str]:
        return self.__categories
