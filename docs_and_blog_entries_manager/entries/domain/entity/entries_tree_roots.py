from typing import Optional

from entries.domain.interface import IConvertibleMarkdownLines
from entries.domain.value import CategoryPath
from .entries_tree import EntriesTree


class EntriesTreeRoots(IConvertibleMarkdownLines):
    """
    CategoryPathと、それに属するEntryをtree状に保持するデータ構造のルートクラス
    """

    def __init__(self, category_path_to_entries_tree: dict[CategoryPath, EntriesTree]):
        self.__category_path_to_entries_tree = category_path_to_entries_tree

    @property
    def root_paths(self) -> list[CategoryPath]:
        return list(self.__category_path_to_entries_tree.keys())

    @property
    def root_trees(self) -> list[EntriesTree]:
        return list(self.__category_path_to_entries_tree.values())

    def get_root_tree(self, category_path: CategoryPath) -> Optional[EntriesTree]:
        if category_path in self.__category_path_to_entries_tree.keys():
            return self.__category_path_to_entries_tree[category_path]
        return None

    def exist(self, category_path: CategoryPath):
        return category_path in self.__category_path_to_entries_tree.keys()

    def search_tree(self, category_path: CategoryPath) -> Optional[EntriesTree]:
        if self.exist(category_path):
            return self.__category_path_to_entries_tree[category_path]
        for path in self.__category_path_to_entries_tree.keys():
            node = self.get_root_tree(path).search_node(category_path)
            if node is not None:
                return node
        return None

    def root_num(self) -> int:
        return len(self.__category_path_to_entries_tree)

    def convert_md_lines(self) -> list[str]:
        lines = []
        for entries_tree in list(self.__category_path_to_entries_tree.values()):
            lines += entries_tree.convert_md_lines()
        return lines
