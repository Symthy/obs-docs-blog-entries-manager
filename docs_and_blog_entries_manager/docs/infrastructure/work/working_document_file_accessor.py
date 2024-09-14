from common.constants import WORK_DOCS_DIR_PATH, NON_CATEGORY_NAME
from docs.domain.datasource.interface import IWorkingDocumentReader, StoredDocEntriesAccessor
from docs.domain.entity import DocEntry
from docs.infrastructure import DocumentFileMover, WorkingDocEntryRestorer
from docs.infrastructure.content.document_category_editor import DocumentCategoryEditor
from files.value import DirectoryPath, FilePath


class WorkingDocumentFileAccessor(IWorkingDocumentReader):
    def __init__(self, stored_doc_entries_accessor: StoredDocEntriesAccessor,
                 document_file_mover: DocumentFileMover,
                 work_doc_dir_path: DirectoryPath = WORK_DOCS_DIR_PATH):
        self.__work_doc_dir_path = work_doc_dir_path
        restorer = WorkingDocEntryRestorer(work_doc_dir_path)
        self.__working_doc_entry_restorer = restorer
        self.__document_category_editor = DocumentCategoryEditor(stored_doc_entries_accessor, work_doc_dir_path)
        self.__document_file_mover = document_file_mover

    def build_file_path(self, title: str) -> FilePath:
        return self.__work_doc_dir_path.add_file(f'{title}.md')

    def restore(self, title: str) -> DocEntry:
        work_doc_file_path = self.build_file_path(title)
        doc_entry = self.__working_doc_entry_restorer.restore(work_doc_file_path)
        self.__document_category_editor.insert_category_path(work_doc_file_path, NON_CATEGORY_NAME)
        return doc_entry

    def extract_completed_filepaths(self) -> list[FilePath]:
        work_file_paths: list[FilePath] = self.__work_doc_dir_path.get_file_paths_in_target_dir()
        completed_file_path: list[FilePath] = list(
            filter(lambda path: self.__working_doc_entry_restorer.restore(path).is_completed, work_file_paths))
        return completed_file_path
