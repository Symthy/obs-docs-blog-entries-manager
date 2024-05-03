from typing import List

from entries.entity.entries_tree import EntriesTree
from entries.interface import IConvertibleMarkdownLines
from store.datasources.stored_entries_accessor import StoredEntriesAccessor
from store.entity.category_tree_definition import CategoryTreeDefinition


class EntriesTreeRoots(IConvertibleMarkdownLines):
    def __init__(self, entries_trees: List[EntriesTree]):
        self.__category_to_entries_tree = {tree.category: tree for tree in entries_trees}

    def convert_md_lines(self) -> List[str]:
        lines = []
        for entries_tree in list(self.__category_to_entries_tree.values()):
            lines += entries_tree.convert_md_lines()
        return lines

    def restore(self, category_tree_definition: CategoryTreeDefinition, stored_entries_accessor: StoredEntriesAccessor):
       for category_path in category_tree_definition.all_category_paths:
           