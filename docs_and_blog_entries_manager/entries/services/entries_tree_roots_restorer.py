# Todo: 外だし
from entries.entity.entries_tree import EntriesTree
from entries.entity.entries_tree_roots import EntriesTreeRoots
from entries.interface import IEntries
from entries.values.category_path import CategoryPath
from store.datasources.stored_entries_accessor import StoredEntriesAccessor
from store.entity.category_tree_definition import CategoryTreeDefinition


class EntriesTreeRootsRestorer:
    def __init__(self, category_tree_definition: CategoryTreeDefinition,
                 stored_entries_accessor: StoredEntriesAccessor):
        self.__category_tree_definition = category_tree_definition
        self.__stored_entries_accessor = stored_entries_accessor

    def execute(self) -> EntriesTreeRoots:
        category_path_to_entries: dict[CategoryPath, IEntries] = self.__build_all_category_path_to_entries()
        return EntriesTreeRoots(self.__convert_to_entries_trees(category_path_to_entries))

    # for testing
    def build_all_category_path_to_entries_for_testing(self) -> dict[CategoryPath, IEntries]:
        return self.__build_all_category_path_to_entries()

    def __build_all_category_path_to_entries(self) -> dict[CategoryPath, IEntries]:
        """
        途中のパスも含めて全CategoryPathを生成
        """
        category_path_to_entries = {}
        for category_full_path in self.__category_tree_definition.category_full_paths:
            entries = self.__stored_entries_accessor.load_entries_by_category_path(category_full_path)
            category_path_to_entries[category_full_path] = entries
            if not category_full_path.exist_parent():
                continue
            for upper_category_path in category_full_path.upper_all_paths():
                if upper_category_path in category_path_to_entries.keys():
                    # 既に探索済みのため skip
                    continue
                entries = self.__stored_entries_accessor.load_entries_by_category_path(upper_category_path)
                category_path_to_entries[upper_category_path] = entries
        return category_path_to_entries

    @staticmethod
    def __convert_to_entries_trees(category_path_to_entries: dict[CategoryPath, IEntries]) -> \
            dict[CategoryPath, EntriesTree]:
        """
        末端のEntryTreeから上層に向けて構築していくことでツリー構築を実現する
        """
        category_path_to_entries_tree = {}
        category_paths = list(category_path_to_entries.keys())
        category_path_ordered_longest_length = sorted(category_paths, key=lambda path: path.length, reverse=True)
        for category_path in category_path_ordered_longest_length:
            child_category_paths = list(
                filter(lambda path: category_path.is_child(path), category_path_to_entries_tree.keys()))
            if len(child_category_paths) == 0:
                # 子category_pathない = 末端
                category_path_to_entries_tree[category_path] = \
                    EntriesTree(category_path, category_path_to_entries[category_path])
                continue
            # 子はEntryTreeはその親EntryTreeに詰めてdictから削除
            child_entries_tree = list(map(lambda path: category_path_to_entries_tree[path], child_category_paths))
            category_path_to_entries_tree[category_path] = \
                EntriesTree(category_path, category_path_to_entries[category_path], child_entries_tree)
            for child_category_path in child_category_paths:
                category_path_to_entries_tree.pop(child_category_path)
        return category_path_to_entries_tree
