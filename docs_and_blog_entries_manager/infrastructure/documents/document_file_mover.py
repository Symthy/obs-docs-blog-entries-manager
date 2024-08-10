from common.constants import DOCS_DIR_PATH
from domain.docs.datasources.interface import IDocumentMover
from files import file_system
from infrastructure.documents.document_file_reader import DocumentFileReader
from infrastructure.types import StoredDocEntriesAccessor


class DocumentFileMover(IDocumentMover):
    def __init__(self, document_file_reader: DocumentFileReader,
                 stored_doc_entries_accessor: StoredDocEntriesAccessor,
                 document_root_dir_path: str = DOCS_DIR_PATH):
        self.__document_root_dir_path = document_root_dir_path
        self.__document_reader = document_file_reader
        self.__stored_doc_entries_accessor = stored_doc_entries_accessor

    def move(self, from_file_path: str, to_file_path: str):
        to_file_path = file_system.join_path(self.__document_root_dir_path, to_file_path)
        file_system.copy_file(from_file_path, to_file_path)
        file_system.remove_file(from_file_path)
        doc_entry = self.__document_reader.restore(to_file_path)
        self.__stored_doc_entries_accessor.save_entry(doc_entry)
