from common.result import Result
from common.results import Results
from domain.docs.entity.doc_entry import DocEntry
from infrastructure.documents.document_file_mover import DocumentFileMover
from infrastructure.documents.work.working_document_file_accessor import WorkingDocumentFileAccessor


class LocalDocPusherService:
    """
    workフォルダの完成記事をdocumentフォルダに格納。手動＆自動(完成基準はタグ付与済みか)
    """

    def __init__(self, working_doc_file_accessor: WorkingDocumentFileAccessor,
                 document_file_mover: DocumentFileMover):
        self.__working_doc_file_accessor = working_doc_file_accessor
        self.__document_file_mover = document_file_mover

    def push(self, title: str) -> Result[DocEntry, str]:
        doc_entry = self.__working_doc_file_accessor.restore(title)
        self.__document_file_mover.move(self.__working_doc_file_accessor.build_file_path(title), doc_entry)
        return Result(doc_entry)

    def push_all(self):
        completed_work_filepaths = self.__working_doc_file_accessor.extract_completed_filepaths()
        results = []
        for file_path in completed_work_filepaths:
            result = self.push(file_path)
            results.append(result)
        return Results(*results)
