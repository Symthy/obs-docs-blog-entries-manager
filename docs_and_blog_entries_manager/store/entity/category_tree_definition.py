from __future__ import annotations

from typing import List

from entries.values.category_path import CategoryPath
from files import file_system
from store.entity.category_group import CategoryGroup


class CategoryTreeDefinition:
    __LOCAL_DOCUMENT_ROOT_DIR_PATH = './docs/'

    def __init__(self, local_document_dir_path: str = None):
        dir_names = file_system.get_dir_names_in_target_dir(
            self.__LOCAL_DOCUMENT_ROOT_DIR_PATH if local_document_dir_path is None else local_document_dir_path)
        categories: dict[str, CategoryGroup] = {}
        for dir_name in dir_names:
            category = self.__build(file_system.join_path(self.__LOCAL_DOCUMENT_ROOT_DIR_PATH, dir_name), dir_name)
            categories[dir_name] = category
        self.__category_name_to_categories = categories

    def __build(self, dir_path: str, target_dir_name: str, parent_category_path: CategoryPath = None) -> CategoryGroup:
        sub_dir_names = file_system.get_dir_names_in_target_dir(dir_path)
        if len(sub_dir_names) == 0:
            return CategoryGroup(self.__build_category_path(target_dir_name, parent_category_path))
        sub_category_groups = []
        for sub_dir in sub_dir_names:
            sub_category_groups.append(self.__build(sub_dir, file_system.join_path(dir_path, sub_dir)))
        return CategoryGroup(self.__build_category_path(target_dir_name, parent_category_path), sub_category_groups)

    @staticmethod
    def __build_category_path(target_dir_name: str, parent_category_path: CategoryPath = None):
        if parent_category_path is None:
            return CategoryPath(target_dir_name)
        return parent_category_path.join(target_dir_name)

    @property
    def all_category_paths(self) -> List[CategoryPath]:
        category_paths = []
        for category_group in self.__category_name_to_categories.values():
            category_paths += category_group.find_category_path()
        return category_paths

    def exist_category_path(self, category_path: str) -> bool:
        category_path_parts = category_path.split('/')
        top_category = category_path_parts[0]
        if top_category in self.__category_name_to_categories.keys():
            return self.__category_name_to_categories[top_category].find_category_path(*category_path_parts[1:])
        return False
