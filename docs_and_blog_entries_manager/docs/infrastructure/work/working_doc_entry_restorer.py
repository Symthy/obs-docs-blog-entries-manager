from common.constants import DOCS_DIR_PATH
from docs.domain.entity import DocEntry
from docs.infrastructure.doc_entry_restorer import _InternalDocEntryRestorer
from files.value import DirectoryPath, FilePath


class WorkingDocEntryRestorer:
    def __init__(self, doc_root_dir_path: DirectoryPath = DOCS_DIR_PATH):
        self.__internal = _InternalDocEntryRestorer(doc_root_dir_path)

    def restore(self, doc_entry_file_path: FilePath) -> DocEntry:
        """
        :raise: DocumentLoadingException
        """
        return self.__internal.restore(doc_entry_file_path)
