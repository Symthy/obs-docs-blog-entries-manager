from common.constants import WORK_DOCS_DIR_PATH, NON_CATEGORY_NAME
from domain.docs.datasources.interface import IWorkingDocumentReader
from domain.docs.entity.doc_entry import DocEntry
from files import file_system
from infrastructure.documents.content.document_category_editor import DocumentCategoryEditor
from infrastructure.documents.doc_entry_restorer import WorkingDocEntryRestorer
from infrastructure.documents.document_file_mover import DocumentFileMover
from infrastructure.types import StoredDocEntriesAccessor


class WorkingDocumentFileAccessor(IWorkingDocumentReader):
    def __init__(self, stored_doc_entries_accessor: StoredDocEntriesAccessor,
                 document_file_mover: DocumentFileMover,
                 work_doc_dir_path: str = WORK_DOCS_DIR_PATH):
        self.__work_doc_dir_path = work_doc_dir_path
        self.__stored_doc_entries_accessor = stored_doc_entries_accessor
        restorer = WorkingDocEntryRestorer(work_doc_dir_path)
        self.__working_doc_entry_restorer = restorer
        self.__document_category_editor = DocumentCategoryEditor(stored_doc_entries_accessor, work_doc_dir_path)
        self.__document_file_mover = document_file_mover

    def build_file_path(self, title: str) -> str:
        return file_system.join_path(self.__work_doc_dir_path, f'{title}.md')

    def restore(self, title: str) -> DocEntry:
        work_doc_file_path = self.build_file_path(title)
        doc_entry = self.__working_doc_entry_restorer.restore(work_doc_file_path)
        self.__document_category_editor.insert_category_path(work_doc_file_path, NON_CATEGORY_NAME)
        return doc_entry

    def extract_completed_filepaths(self) -> list[str]:
        work_file_paths = file_system.get_file_paths_in_target_dir(self.__work_doc_dir_path)
        completed_file_path = list(
            filter(lambda path: self.__working_doc_entry_restorer.restore(path).is_completed, work_file_paths))
        return completed_file_path
