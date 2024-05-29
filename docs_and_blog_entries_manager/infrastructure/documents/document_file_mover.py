from common.constants import DOCS_DIR_PATH
from domain.docs.datasources.interface import IDocumentMover
from domain.docs.entity.doc_entry import DocEntry
from files import file_system


class DocumentFileMover(IDocumentMover):
    def __init__(self):
        self.__document_root_path = DOCS_DIR_PATH

    def move(self, from_file_path: str, doc_entry: DocEntry):
        to_file_path = file_system.join_path(self.__document_root_path, doc_entry.doc_file_path)
        file_system.copy_file(from_file_path, to_file_path)
        file_system.remove_file(from_file_path)
