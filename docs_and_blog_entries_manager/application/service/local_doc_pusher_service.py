from common.constants import NON_CATEGORY_NAME
from common.result import Result
from common.results import Results
from domain.docs.datasources.interface import IDocumentAccessor, IDocumentMover
from domain.docs.entity.doc_entry import DocEntry
from infrastructure.documents.doc_entry_restorer import DocumentReader
from infrastructure.documents.work.working_document_file_accessor import WorkingDocumentFileAccessor
from infrastructure.types import StoredDocEntriesAccessor


class LocalDocPusherService:
    """
    workフォルダの完成記事をdocumentフォルダに格納。手動＆自動(完成基準はタグ付与済みか)
    """

    def __init__(self, stored_doc_entries_accessor: StoredDocEntriesAccessor, doc_entry_restorer: DocumentReader,
                 document_file_accessor: IDocumentAccessor, document_file_mover: IDocumentMover,
                 working_doc_file_accessor: WorkingDocumentFileAccessor):
        self.__stored_doc_entries_accessor = stored_doc_entries_accessor
        self.__doc_entry_restorer = doc_entry_restorer
        self.__document_file_accessor = document_file_accessor
        self.__document_file_mover = document_file_mover
        self.__working_doc_file_accessor = working_doc_file_accessor

    def push(self, title: str) -> Result[DocEntry, str]:
        work_doc_file_path = self.__working_doc_file_accessor.build_file_path(title)
        doc_entry = self.__doc_entry_restorer.restore(work_doc_file_path)
        self.__document_file_accessor.insert_category_path(work_doc_file_path, NON_CATEGORY_NAME)
        self.__document_file_mover.move(work_doc_file_path, doc_entry)
        self.__stored_doc_entries_accessor.save_entry(doc_entry)
        return Result(doc_entry)

    def push_all(self):
        completed_work_filepaths = self.__working_doc_file_accessor.extract_completed_filepaths()
        results = []
        for file_path in completed_work_filepaths:
            result = self.push(file_path)
            results.append(result)
        return Results(*results)
