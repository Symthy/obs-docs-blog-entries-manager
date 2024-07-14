from typing import List

from common.constants import WORK_DOCS_DIR_PATH, NON_CATEGORY_NAME
from files import file_system
from infrastructure.documents.document_file_accessor import DocumentFileAccessor
from infrastructure.documents.document_file_mover import DocumentFileMover
from infrastructure.documents.document_file_reader import DocumentFileReader
from infrastructure.types import StoredDocEntriesAccessor


class WorkingDocumentFileAccessor:
    def __init__(self, stored_doc_entries_accessor: StoredDocEntriesAccessor,
                 document_file_accessor: DocumentFileAccessor, document_file_mover: DocumentFileMover,
                 work_doc_dir_path: str = WORK_DOCS_DIR_PATH):
        self.__work_doc_dir_path = work_doc_dir_path
        self.__stored_doc_entries_accessor = stored_doc_entries_accessor
        self.__work_document_file_reader = DocumentFileReader(work_doc_dir_path, stored_doc_entries_accessor)
        self.__document_file_accessor = document_file_accessor
        self.__document_file_mover = document_file_mover

    def extract_completed_filepaths(self) -> List[str]:
        work_file_paths = file_system.get_file_paths_in_target_dir(self.__work_doc_dir_path)
        completed_file_path = list(
            filter(lambda path: self.__work_document_file_reader.restore(path).is_completed, work_file_paths))
        return completed_file_path

    def restore(self, title: str):
        work_doc_file_path = self.build_file_path(title)
        doc_entry = self.__work_document_file_reader.restore(work_doc_file_path)
        self.__document_file_accessor.insert_category_path(work_doc_file_path, NON_CATEGORY_NAME)
        return doc_entry

    def build_file_path(self, title: str) -> str:
        return file_system.join_path(self.__work_doc_dir_path, f'{title}.md')
