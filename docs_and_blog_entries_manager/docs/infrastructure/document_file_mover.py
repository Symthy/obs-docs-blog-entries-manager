from common.constants import DOCS_DIR_PATH
from docs.domain.datasource.interface import IDocumentMover, StoredDocEntriesAccessor
from docs.infrastructure import DocumentFileReader
from files.value import FilePath, DirectoryPath


class DocumentFileMover(IDocumentMover):
    def __init__(self, document_file_reader: DocumentFileReader,
                 stored_doc_entries_accessor: StoredDocEntriesAccessor,
                 document_root_dir_path: DirectoryPath = DOCS_DIR_PATH):
        self.__document_root_dir_path = document_root_dir_path
        self.__document_reader = document_file_reader
        self.__stored_doc_entries_accessor = stored_doc_entries_accessor

    def move(self, from_file_path: FilePath, to_file_path: FilePath):
        to_file_path = self.__document_root_dir_path.join_file_path(to_file_path)
        from_file_path.copy_file(to_file_path)
        from_file_path.remove_file()
        doc_entry = self.__document_reader.restore(to_file_path)
        self.__stored_doc_entries_accessor.save_entry(doc_entry)
