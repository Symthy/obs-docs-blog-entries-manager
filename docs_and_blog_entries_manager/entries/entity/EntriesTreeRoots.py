from typing import List

from entries.entity.entries_tree import EntriesTree
from entries.interface import IConvertibleMarkdownLines


class EntriesTreeRoots(IConvertibleMarkdownLines):
    def __init__(self, entries_trees: List[EntriesTree]):
        self.__category_to_entries_tree = {tree.category: tree for tree in entries_trees}

    def convert_md_lines(self) -> List[str]:
        lines = []
        for entries_tree in list(self.__category_to_entries_tree.values()):
            lines += entries_tree.convert_md_lines()
        return lines
