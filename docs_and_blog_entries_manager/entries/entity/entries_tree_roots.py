from typing import List

from entries.entity.entries_tree import EntriesTree
from entries.interface import IConvertibleMarkdownLines, IEntries
from entries.values.category_path import CategoryPath
from store.datasources.stored_entries_accessor import StoredEntriesAccessor
from store.entity.category_tree_definition import CategoryTreeDefinition


class EntriesTreeRoots(IConvertibleMarkdownLines):
    def __init__(self, entries_trees: List[EntriesTree]):
        self.__category_path_to_entries_tree: dict[CategoryPath, EntriesTree] = \
            {tree.category_path: tree for tree in entries_trees}

    def convert_md_lines(self) -> List[str]:
        lines = []
        for entries_tree in list(self.__category_to_entries_tree.values()):
            lines += entries_tree.convert_md_lines()
        return lines

    # Todo: 外だし
    def restore(self, category_tree_definition: CategoryTreeDefinition, stored_entries_accessor: StoredEntriesAccessor):
        category_path_to_entries: dict[CategoryPath, IEntries] = {}
        # 全category_path抽出
        for category_full_path in category_tree_definition.category_full_paths:
            entries = stored_entries_accessor.load_entries_by_category_path(category_full_path)
            category_path_to_entries[category_full_path] = entries
            if not category_full_path.exist_parent():
                continue
            for upper_category_path in category_full_path.upper_all_paths():
                if upper_category_path in category_path_to_entries.keys():
                    # 既に探索済みのため skip
                    continue
                entries = stored_entries_accessor.load_entries_by_category_path(upper_category_path)
                category_path_to_entries[upper_category_path] = entries
        # 末端のEntryTreeから上層に構築していくことでツリー構築を実現する
        category_path_to_entries_tree = {}
        category_paths = list(category_path_to_entries.keys())
        category_path_ordered_longest_length = sorted(category_paths, key=lambda path: path.length, reverse=True)
        for category_path in category_path_ordered_longest_length:
            child_category_paths = list(
                filter(lambda path: path.is_child(category_path), category_path_to_entries_tree.keys()))
            if len(child_category_paths) == 0:
                # 子category_pathない = 末端なら
                category_path_to_entries_tree[category_path] = \
                    EntriesTree(category_path, category_path_to_entries[category_path])
                continue
            # 子category_pathがあるなら、子はEntryTreeはその親EntryTreeに詰めてdictから削除
            child_entries_tree = list(map(lambda path: category_path_to_entries_tree[path], child_category_paths))
            category_path_to_entries_tree[category_path] = \
                EntriesTree(category_path, category_path_to_entries[category_path], child_entries_tree)
            for child_category_path in child_category_paths:
                category_path_to_entries_tree.pop(child_category_path)
        self.__category_path_to_entries_tree = category_path_to_entries_tree
