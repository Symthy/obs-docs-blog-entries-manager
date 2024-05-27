from common.constants import NON_CATEGORY_NAME, WORK_DOCS_DIR_PATH
from domain.docs.entity.doc_entry import DocEntry
from files import file_system
from infrastructure.documents.doc_entry_restorer import DocEntryRestorer
from infrastructure.documents.document_file_accessor import DocumentFileAccessor
from infrastructure.documents.document_file_mover import DocumentFileMover
from infrastructure.types import StoredDocEntriesAccessor


class LocalDocPusherService:
    """
    workフォルダの完成記事をdocumentフォルダに格納。手動＆自動(完成基準はタグ付与済みか)
    """

    def __init__(self, stored_doc_entries_accessor: StoredDocEntriesAccessor, doc_entry_restorer: DocEntryRestorer,
                 document_file_accessor: DocumentFileAccessor, document_file_mover: DocumentFileMover,
                 work_doc_dir_path: str = WORK_DOCS_DIR_PATH):
        self.__stored_doc_entries_accessor = stored_doc_entries_accessor
        self.__doc_entry_restorer = doc_entry_restorer
        self.__document_file_accessor = document_file_accessor
        self.__document_file_mover = document_file_mover
        self.__work_doc_dir_path = work_doc_dir_path

    def execute(self, title: str) -> DocEntry:
        work_doc_file_path = self.__build_file_path(title)
        doc_entry = self.__doc_entry_restorer.execute(work_doc_file_path)
        self.__document_file_accessor.insert_category_path(work_doc_file_path, NON_CATEGORY_NAME)
        self.__document_file_mover.move(work_doc_file_path, doc_entry)
        self.__stored_doc_entries_accessor.save_entry(doc_entry)
        return doc_entry

    def __build_file_path(self, title: str) -> str:
        return file_system.join_path(self.__work_doc_dir_path, f'{title}.md')
