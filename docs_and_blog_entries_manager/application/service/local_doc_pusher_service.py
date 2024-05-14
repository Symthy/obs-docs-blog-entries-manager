from common.constants import NON_CATEGORY_NAME
from infrastructure.documents.doc_entry_restorer import DocEntryRestorer
from infrastructure.documents.document_file_accessor import DocumentFileAccessor
from infrastructure.documents.document_file_mover import DocumentFileMover
from infrastructure.types import StoredDocEntriesAccessor


class LocalDocPusherService:
    def __init__(self, stored_doc_entries_accessor: StoredDocEntriesAccessor, doc_entry_restorer: DocEntryRestorer,
                 document_file_accessor: DocumentFileAccessor, document_file_mover: DocumentFileMover):
        self.__stored_doc_entries_accessor = stored_doc_entries_accessor
        self.__doc_entry_restorer = doc_entry_restorer
        self.__document_file_accessor = document_file_accessor
        self.__document_file_mover = document_file_mover

    def execute(self, work_doc_file_path):
        doc_entry = self.__doc_entry_restorer.execute(work_doc_file_path)
        self.__document_file_accessor.insert_category_path_to_content(work_doc_file_path, NON_CATEGORY_NAME)
        self.__document_file_mover.move(work_doc_file_path, doc_entry)
        self.__stored_doc_entries_accessor.save_entry(doc_entry)
