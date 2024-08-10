from typing import List

from domain.docs.datasources.interface import IDocumentReader, IDocumentMover
from domain.docs.entity.doc_entry import DocEntry
from domain.entries.entity.category_tree_definition import CategoryTreeDefinition
from domain.entries.values.category_path import CategoryPath
from infrastructure.types import StoredDocEntriesAccessor


class LocalDocOrganizerService:
    """
    documentフォルダ内の記事を記事のカテゴリパスに応じて整理(移動)
    """

    def __init__(self, category_tree_def: CategoryTreeDefinition,
                 document_file_mover: IDocumentMover,
                 document_file_reader: IDocumentReader,
                 stored_doc_entries_accessor: StoredDocEntriesAccessor):
        self.__category_tree_def = category_tree_def
        self.__document_file_mover = document_file_mover
        self.__document_file_reader = document_file_reader
        self.__stored_doc_entries_accessor = stored_doc_entries_accessor

    def organize(self):
        category_paths: List[CategoryPath] = self.__category_tree_def.all_category_paths
        # Todo: refactor
        for category_path in category_paths:
            doc_file_paths = self.__category_tree_def.get_file_paths(category_path)
            for doc_file_path in doc_file_paths:
                current_doc_entry: DocEntry = self.__document_file_reader.restore(doc_file_path)
                old_doc_entry: DocEntry = self.__stored_doc_entries_accessor.load_entry(current_doc_entry.id)
                if not current_doc_entry.equals_path(old_doc_entry):
                    self.__document_file_mover.move(old_doc_entry.doc_file_path, current_doc_entry.doc_file_path)
