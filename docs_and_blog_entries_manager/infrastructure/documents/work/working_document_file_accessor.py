from typing import List

from common.constants import WORK_DOCS_DIR_PATH
from files import file_system
from infrastructure.documents.doc_entry_restorer import DocumentReader


class WorkingDocumentFileAccessor:
    def __init__(self, work_doc_dir_path: str = WORK_DOCS_DIR_PATH):
        self.__work_doc_dir_path = work_doc_dir_path
        self.__doc_entry_restorer = DocumentReader(work_doc_dir_path)

    def extract_completed_filepaths(self) -> List[str]:
        work_file_paths = file_system.get_file_paths_in_target_dir(self.__work_doc_dir_path)
        completed_file_path = list(
            filter(lambda path: self.__doc_entry_restorer.restore(path).is_completed, work_file_paths))
        return completed_file_path

    def build_file_path(self, title: str) -> str:
        # Todo: error case
        return file_system.join_path(self.__work_doc_dir_path, f'{title}.md')
