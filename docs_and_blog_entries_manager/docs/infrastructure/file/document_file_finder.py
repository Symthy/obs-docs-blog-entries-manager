from common.constants import DOCS_DIR_PATH
from docs.domain.datasource.interface import StoredDocEntriesAccessor
from docs.domain.entity import DocumentDataset
from docs.domain.value import DocEntryId
from docs.infrastructure.content.document_content_reader import DocumentContentReader
from files.value import DirectoryPath


class DocumentFileFinder:
    def __init__(self, stored_doc_entries_accessor: StoredDocEntriesAccessor,
                 doc_root_dir_path: DirectoryPath = DOCS_DIR_PATH):
        self.__doc_root_dir_path: DirectoryPath = doc_root_dir_path
        self.__stored_doc_entries_accessor = stored_doc_entries_accessor
        self.__doc_content_reader = DocumentContentReader()

    def find(self, doc_id: DocEntryId) -> DocumentDataset:
        """
        :raise: DocumentLoadingException
        """
        doc_entry = self.__stored_doc_entries_accessor.load_entry(doc_id)
        doc_file_path = self.__doc_root_dir_path.join_file_path(doc_entry.doc_file_path)
        # delegate
        content = self.__doc_content_reader.load(doc_file_path)
        return DocumentDataset(doc_entry, content)
