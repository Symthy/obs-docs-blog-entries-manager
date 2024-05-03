from __future__ import annotations

from typing import List

from files import file_system


class CategoryGroup:
    """
    直下のカテゴリまでを保持するクラス
    """

    def __init__(self, category: str, category_children: List[CategoryGroup] = None):
        self.__category = category
        self.__children: List[CategoryGroup] = [] if category_children is None else category_children

    @property
    def category(self) -> str:
        return self.__category

    @property
    def sub_categories(self) -> List[str]:
        return [child.category for child in self.__children]


class CategoryTreeDefinition:
    __LOCAL_DOCUMENT_ROOT_DIR_PATH = './docs/'

    def __init__(self):
        dir_names = file_system.get_dir_names_in_target_dir(self.__LOCAL_DOCUMENT_ROOT_DIR_PATH)
        categories: List[CategoryGroup] = []
        for dir in dir_names:
            categories.append(self.__build(dir, file_system.join_path(self.__LOCAL_DOCUMENT_ROOT_DIR_PATH, dir)))
        self.__categories = categories

    def __build(self, target_dir_name: str, dir_path: str) -> CategoryGroup:
        sub_dir_names = file_system.get_dir_names_in_target_dir(dir_path)
        if len(sub_dir_names) == 0:
            return CategoryGroup(target_dir_name)

        sub_category_groups = []
        for sub_dir in sub_dir_names:
            sub_category_groups.append(self.__build(sub_dir, file_system.join_path(dir_path, sub_dir)))
        return CategoryGroup(target_dir_name, sub_category_groups)
