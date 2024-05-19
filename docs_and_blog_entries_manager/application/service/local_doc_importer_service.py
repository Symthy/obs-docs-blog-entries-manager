from typing import List

from domain.docs.entity.doc_entries import DocEntries
from domain.entries.entity.category_tree_definition import CategoryTreeDefinition
from domain.entries.values.category_path import CategoryPath
from infrastructure.documents.document_file_accessor import DocumentFileAccessor
from infrastructure.types import StoredDocEntriesAccessor
from logs.logger import Logger


class LocalDocImporterService:
    """
    documentフォルダに直接作成された未登録記事を認識＆登録
    """

    def __init__(self, category_tree_def: CategoryTreeDefinition, document_file_accessor: DocumentFileAccessor,
                 stored_doc_entries_accessor: StoredDocEntriesAccessor):
        self.__category_tree_def = category_tree_def
        self.__document_file_accessor = document_file_accessor
        self.__stored_doc_entries_accessor = stored_doc_entries_accessor

    def execute(self):
        """
        内部保持のEntry一覧にあるか確認して、ないものは登録。記事にカテゴリ付与も行う
        """
        all_category_paths: List[CategoryPath] = self.__category_tree_def.all_category_paths
        non_exist_doc_entries: DocEntries = self.__document_file_accessor.find_non_register_doc_entries(
            list(map(lambda path: path.value, all_category_paths)))
        if non_exist_doc_entries.is_empty():
            Logger.info('Nothing new document.')
            return
        self.__stored_doc_entries_accessor.save_entries(non_exist_doc_entries)
        for doc_entry in non_exist_doc_entries.items:
            self.__document_file_accessor.insert_category_path_to_content(doc_entry.doc_file_path,
                                                                          doc_entry.category_path)
