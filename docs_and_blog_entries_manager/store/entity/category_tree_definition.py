from __future__ import annotations

from typing import List

from entries.values.category_path import CategoryPath
from files import file_system
from store.entity.category_group import CategoryGroup


class CategoryTreeDefinition:
    __LOCAL_DOCUMENT_ROOT_DIR_PATH = './docs/'

    def __init__(self, category_name_to_categories: dict[str, CategoryGroup] = None):
        self.__category_name_to_categories = category_name_to_categories if category_name_to_categories is not None else {}

    @classmethod
    def build(cls, local_document_dir_path):
        dir_names = file_system.get_dir_names_in_target_dir(
            cls.__LOCAL_DOCUMENT_ROOT_DIR_PATH if local_document_dir_path is None else local_document_dir_path)
        categories: dict[str, CategoryGroup] = {}
        for dir_name in dir_names:
            dir_full_path = file_system.join_path(cls.__LOCAL_DOCUMENT_ROOT_DIR_PATH, dir_name)
            category_group = cls.__build_category_group(dir_full_path, dir_name)
            categories[dir_name] = category_group
        return CategoryTreeDefinition(categories)

    def __build_category_group(self, dir_path: str, target_dir_name: str,
                               parent_category_path: CategoryPath = None) -> CategoryGroup:
        sub_dir_names = file_system.get_dir_names_in_target_dir(dir_path)
        if len(sub_dir_names) == 0:
            return CategoryGroup(self.__build_category_path(target_dir_name, parent_category_path))
        sub_category_groups = []
        for sub_dir in sub_dir_names:
            sub_category_groups.append(self.__build_category_group(sub_dir, file_system.join_path(dir_path, sub_dir)))
        return CategoryGroup(self.__build_category_path(target_dir_name, parent_category_path), sub_category_groups)

    @staticmethod
    def __build_category_path(target_dir_name: str, parent_category_path: CategoryPath = None):
        if parent_category_path is None:
            return CategoryPath(target_dir_name)
        return parent_category_path.join(target_dir_name)

    @property
    def category_full_paths(self) -> List[CategoryPath]:
        """
        フルパスの category_path のみ取得。途中階層のパスは含めない
        """
        category_paths = []
        for category_group in self.__category_name_to_categories.values():
            category_paths += category_group.category_paths()
        return category_paths

    def exist_category_path(self, category_path_str: str) -> bool:
        category_path = CategoryPath(category_path_str)
        if category_path.top in self.__category_name_to_categories.keys():
            return self.__category_name_to_categories[category_path.top].find_category_path(category_path)
        return False
