from common.constants import DOCS_DIR_PATH
from domain.docs.datasource.interface import StoredDocEntriesAccessor
from domain.entries.entity.category_tree_definition import CategoryTreeDefinition
from infrastructure.documents.document_file_accessor import DocumentFileAccessor
from infrastructure.documents.document_file_reader import DocumentFileReader
from infrastructure.documents.file.all_document_path_resolver import AllDocumentPathResolver
from infrastructure.store.stored_entry_list_holder import StoredEntryListHolder


class DocumentFileAccessorFactory:
    def __init__(self, stored_doc_entries_accessor: StoredDocEntriesAccessor,
                 stored_doc_entry_list: StoredEntryListHolder,
                 category_tree_def: CategoryTreeDefinition,
                 doc_root_dir_path: str = DOCS_DIR_PATH):
        self.__doc_root_dir_path = doc_root_dir_path
        self.__stored_doc_entries_accessor = stored_doc_entries_accessor
        self.__stored_doc_entry_list = stored_doc_entry_list
        self.__category_tree_def = category_tree_def

    def build(self) -> DocumentFileAccessor:
        resolver = AllDocumentPathResolver(self.__category_tree_def, self.__doc_root_dir_path)
        reader = DocumentFileReader(self.__stored_doc_entries_accessor, self.__stored_doc_entry_list, resolver,
                                    self.__doc_root_dir_path)
        accessor = DocumentFileAccessor(self.__stored_doc_entries_accessor, reader, self.__doc_root_dir_path)
        return accessor
