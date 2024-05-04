from typing import List, Optional

from entries.entity.entries_tree import EntriesTree
from entries.interface import IConvertibleMarkdownLines
from entries.values.category_path import CategoryPath


class EntriesTreeRoots(IConvertibleMarkdownLines):
    def __init__(self, category_path_to_entries_tree: dict[CategoryPath, EntriesTree]):
        self.__category_path_to_entries_tree = category_path_to_entries_tree

    def get_root_paths(self) -> List[CategoryPath]:
        return list(self.__category_path_to_entries_tree.keys())

    def get_top_tree(self, category_path: CategoryPath) -> Optional[EntriesTree]:
        if category_path in self.__category_path_to_entries_tree.keys():
            return self.__category_path_to_entries_tree[category_path]
        return None

    def exist(self, category_path: CategoryPath):
        return category_path in self.__category_path_to_entries_tree.keys()

    def search_tree(self, category_path: CategoryPath) -> Optional[EntriesTree]:
        if self.exist(category_path):
            return self.__category_path_to_entries_tree[category_path]
        for path in self.__category_path_to_entries_tree.keys():
            node = self.get_top_tree(path).search_node(category_path)
            if node is not None:
                return node
        return None

    def root_num(self) -> int:
        return len(self.__category_path_to_entries_tree)

    def convert_md_lines(self) -> List[str]:
        lines = []
        for entries_tree in list(self.__category_path_to_entries_tree.values()):
            lines += entries_tree.convert_md_lines()
        return lines
