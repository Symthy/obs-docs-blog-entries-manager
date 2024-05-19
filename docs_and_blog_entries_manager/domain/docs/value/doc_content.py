from __future__ import annotations

import re
from typing import List, Optional

from common.constants import NON_CATEGORY_NAME
from domain.entries.values.category_path import CategoryPath
from files import file_system


class DocContent:
    __DOCUMENT_IMAGE_LINK_REGEX = r'!\[.*\]\((.+)\)'
    __DOCUMENT_CATEGORY_REGEX = r'#(\S+)'

    def __init__(self, content: str, doc_entry_dir_path: str):
        self.__content = content if content.endswith('\n') else content + '\n'
        self.__doc_entry_dir_path = doc_entry_dir_path
        self.__image_paths_from_doc_file = self.__extract_image_paths(doc_entry_dir_path)
        all_categories = self.__extract_categories()
        self.__categories = all_categories[1:] if len(all_categories) >= 2 else []
        self.__category_path = self.__categories[0] if len(all_categories) >= 1 else None
        if self.__category_path is None:
            self.__category_path = CategoryPath(NON_CATEGORY_NAME)
            self.__content += f'#{self.__category_path.value}\n'

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
    def image_paths_from_doc_file(self) -> List[str]:
        return self.__image_paths_from_doc_file

    @property
    def image_paths(self) -> List[str]:
        return list(
            map(lambda path: file_system.join_path(self.__category_path.value, path), self.__image_paths_from_doc_file))

    @property
    def category_path(self) -> Optional[CategoryPath]:
        return self.__category_path

    @property
    def not_exist_category_path(self) -> bool:
        return self.__category_path is None

    def add_category(self, category_path: CategoryPath, categories: List[str]) -> DocContent:
        new_category_line = ' '.join(list(map(lambda c: f'#{c}', [category_path.value, *categories]))) + '\n'
        new_content = self.value_with_removed_categories + new_category_line
        return DocContent(new_content, self.__doc_entry_dir_path)

    def remove_category(self, category_to_be_removed: str):
        new_categories = [category for category in self.__categories if category != category_to_be_removed]
        new_category_line = ' '.join(list(map(lambda c: f'#{c}', [self.category_path.value, *new_categories]))) + '\n'
        new_content = self.value_with_removed_categories + new_category_line
        return DocContent(new_content, self.__doc_entry_dir_path)

    @property
    def categories(self) -> List[str]:
        return self.__categories
