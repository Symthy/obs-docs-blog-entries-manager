from common.constants import DOCS_DIR_PATH
from docs.domain.datasource.interface import StoredDocEntriesAccessor, IDocumentAccessor
from docs.infrastructure import DocumentFileAccessor
from docs.infrastructure import DocumentFileReader
from docs.infrastructure.file import AllDocumentPathResolver
from docs.infrastructure.types import StoredDocEntryListHolder
from entries.domain.entity import CategoryTreeDefinition
from files.value import DirectoryPath


class DocumentFileAccessorFactory:
    def __init__(self, stored_doc_entries_accessor: StoredDocEntriesAccessor,
                 stored_doc_entry_list: StoredDocEntryListHolder,
                 category_tree_def: CategoryTreeDefinition,
                 doc_root_dir_path: DirectoryPath = DOCS_DIR_PATH):
        self.__doc_root_dir_path = doc_root_dir_path
        self.__stored_doc_entries_accessor = stored_doc_entries_accessor
        self.__stored_doc_entry_list = stored_doc_entry_list
        self.__category_tree_def = category_tree_def

    def build(self) -> IDocumentAccessor:
        resolver = AllDocumentPathResolver(self.__category_tree_def, self.__doc_root_dir_path)
        reader = DocumentFileReader(self.__stored_doc_entries_accessor, self.__stored_doc_entry_list, resolver,
                                    self.__doc_root_dir_path)
        accessor = DocumentFileAccessor(self.__stored_doc_entries_accessor, reader, self.__doc_root_dir_path)
        return accessor
