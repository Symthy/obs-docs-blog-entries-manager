from typing import List

from domain.docs.entity.doc_entries import DocEntries
from domain.entries.entity.category_tree_definition import CategoryTreeDefinition
from domain.entries.values.category_path import CategoryPath
from infrastructure.documents.document_file_accessor import DocumentFileAccessor
from infrastructure.store.stored_entry_list_holder import StoredEntryListHolder
from logs.logger import Logger


class LocalDocImporterService:
    def __init__(self, category_tree_def: CategoryTreeDefinition, document_file_accessor: DocumentFileAccessor,
                 stored_entry_list_holder: StoredEntryListHolder):
        self.__category_tree_def = category_tree_def
        self.__document_file_accessor = document_file_accessor
        self.__stored_entry_list_holder = stored_entry_list_holder

    def __execute(self):
        """
        一覧にあるか確認して、ないものは追加。カテゴリ付与もいる
        """
        all_category_paths: List[CategoryPath] = self.__category_tree_def.all_categoory_paths
        non_exist_doc_entries: DocEntries = self.__document_file_accessor.find_non_register_doc_entries(
            list(map(lambda path: path.value, all_category_paths)))
        if non_exist_doc_entries.is_empty():
            Logger.info('Nothing new document.')
            return
        self.__stored_entry_list_holder.push_entries(non_exist_doc_entries)
        for doc_entry in non_exist_doc_entries.items:
            self.__document_file_accessor.insert_category_path_to_content(doc_entry.doc_file_path,
                                                                          doc_entry.category_path)
