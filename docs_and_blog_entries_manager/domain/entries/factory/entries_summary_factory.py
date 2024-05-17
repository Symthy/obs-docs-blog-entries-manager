from domain.entries.entity.category_tree_definition import CategoryTreeDefinition
from domain.entries.entity.entries_summary import EntriesSummary
from domain.entries.interface import IStoredEntriesAccessor
from domain.entries.services.entries_tree_roots_restorer import EntriesTreeRootsRestorer


class EntriesSummaryFactory:
    def __init__(self, document_root_dir_path: str, summary_entry_title: str,
                 stored_entries_accessor: IStoredEntriesAccessor):
        self.__summary_entry_title = summary_entry_title
        self.__document_root_dir_path = document_root_dir_path
        self.__stored_entries_accessor = stored_entries_accessor

    def build(self):
        category_tree_def = CategoryTreeDefinition.build(self.__document_root_dir_path)
        entries_tree_roots_restorer = EntriesTreeRootsRestorer(category_tree_def, self.__stored_entries_accessor)
        entries_tree_roots = entries_tree_roots_restorer.execute()
        return EntriesSummary(self.__summary_entry_title, entries_tree_roots)
