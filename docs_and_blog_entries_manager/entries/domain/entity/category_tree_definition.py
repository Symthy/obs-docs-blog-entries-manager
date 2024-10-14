from __future__ import annotations

from typing import Optional

from common.constants import DOCS_DIR_PATH
from entries.domain.value import CategoryPath
from files.value.file_path import FilePath, DirectoryPath
from .category_group import CategoryGroup


class CategoryTreeDefinition:
    """
    ローカルドキュメントのすべてのフォルダパス（CategoryPath）をTree形式で保持する物
    """
    __LOCAL_DOCUMENT_ROOT_DIR_PATH: DirectoryPath = DOCS_DIR_PATH

    def __init__(self, category_name_to_categories: dict[str, CategoryGroup] = None):
        self.__category_name_to_categories = category_name_to_categories if category_name_to_categories is not None else {}

    @classmethod
    def build(cls, document_root_dir_path: DirectoryPath = None):
        dir_path = cls.__LOCAL_DOCUMENT_ROOT_DIR_PATH if document_root_dir_path is None else document_root_dir_path
        dir_names = dir_path.get_dir_name_from_dir_path()
        categories: dict[str, CategoryGroup] = {}
        for dir_name in dir_names:
            dir_full_path = cls.__LOCAL_DOCUMENT_ROOT_DIR_PATH.add_dir(dir_name)
            category_group = cls.__build_category_group(dir_full_path, dir_name)
            categories[dir_name] = category_group
        return CategoryTreeDefinition(categories)

    @property
    def category_full_paths(self) -> list[CategoryPath]:
        """
        フルパスの category_path のみ取得。途中階層のパスは含めない
        """
        category_paths = []
        for category_group in self.__category_name_to_categories.values():
            category_paths += category_group.category_full_paths()
        return category_paths

    @property
    def all_category_paths(self) -> list[CategoryPath]:
        """
        途中階層も含めて全ての category_path を取得
        """
        category_paths = []
        for category_group in self.__category_name_to_categories.values():
            category_paths += category_group.all_category_paths()
        return category_paths

    def exist_category_path(self, category_path: CategoryPath) -> bool:
        if category_path.top in self.__category_name_to_categories.keys():
            return self.__category_name_to_categories[category_path.top].find_category_path(category_path)
        return False

    def get_file_paths(self, category_path: CategoryPath) -> list[FilePath]:
        target_dir_path = self.__LOCAL_DOCUMENT_ROOT_DIR_PATH.join(category_path.value)
        return target_dir_path.get_file_paths_in_target_dir()

    @classmethod
    def __build_category_group(cls, dir_path: DirectoryPath, target_dir_name: str,
                               parent_category_path: Optional[CategoryPath] = None) -> CategoryGroup:
        sub_dir_names = dir_path.get_dir_name_from_dir_path()
        if len(sub_dir_names) == 0:
            return CategoryGroup(cls.__build_category_path(target_dir_name, parent_category_path))
        sub_category_groups = []
        for sub_dir_name in sub_dir_names:
            sub_category_groups.append(cls.__build_category_group(dir_path.add_dir(sub_dir_name), sub_dir_name))
        return CategoryGroup(cls.__build_category_path(target_dir_name, parent_category_path), sub_category_groups)

    @staticmethod
    def __build_category_path(target_dir_name: str, parent_category_path: CategoryPath = None):
        if parent_category_path is None:
            return CategoryPath(target_dir_name)
        return parent_category_path.join(target_dir_name)
