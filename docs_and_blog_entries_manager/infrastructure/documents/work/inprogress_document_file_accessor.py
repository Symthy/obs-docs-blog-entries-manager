from typing import List

from files import file_system
from infrastructure.documents.doc_entry_restorer import DocEntryRestorer


class InprogressDocumentFileAccessor:
    def __init__(self, work_dir_path: str):
        self.__work_dir_path = work_dir_path
        self.__doc_entry_restorer = DocEntryRestorer(work_dir_path)

    def extract_completed_filepaths(self) -> List[str]:
        work_file_paths = file_system.get_file_paths_in_target_dir(self.__work_dir_path)
        completed_file_path = list(
            filter(lambda path: self.__doc_entry_restorer.execute(path).is_completed, work_file_paths))
        return completed_file_path
