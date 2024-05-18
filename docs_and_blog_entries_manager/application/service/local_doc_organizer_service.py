from typing import List

from domain.docs.entity.doc_entry import DocEntry
from domain.entries.entity.category_tree_definition import CategoryTreeDefinition
from domain.entries.values.category_path import CategoryPath
from infrastructure.documents.doc_entry_restorer import DocEntryRestorer
from infrastructure.documents.document_file_accessor import DocumentFileAccessor
from infrastructure.documents.document_file_mover import DocumentFileMover
from infrastructure.types import StoredDocEntriesAccessor


class LocalDocOrganizerService:
    def __init__(self, category_tree_def: CategoryTreeDefinition, document_file_accessor: DocumentFileAccessor,
                 document_file_mover: DocumentFileMover, doc_entry_restorer: DocEntryRestorer,
                 stored_doc_entries_accessor: StoredDocEntriesAccessor):
        self.__category_tree_def = category_tree_def
        self.__document_file_accessor = document_file_accessor
        self.__document_file_mover = document_file_mover
        self.__doc_entry_restorer = doc_entry_restorer
        self.__stored_doc_entries_accessor = stored_doc_entries_accessor

    def organize(self):
        category_paths: List[CategoryPath] = self.__category_tree_def.all_category_paths
        for category_path in category_paths:
            doc_file_paths = self.__document_file_accessor.get_file_paths(category_path)
            for doc_file_path in doc_file_paths:
                current_doc_entry: DocEntry = self.__doc_entry_restorer.execute(doc_file_path)
                old_doc_entry: DocEntry = self.__stored_doc_entries_accessor.load_entry(current_doc_entry.id)
                if not current_doc_entry.equals_path(old_doc_entry):
                    self.__document_file_mover.move(doc_file_path, current_doc_entry)
                    self.__stored_doc_entries_accessor.save_entry(current_doc_entry)
