from common.result import Result
from common.results import Results
from domain.docs.entity.doc_entry import DocEntry
from infrastructure.documents.work.working_document_file_accessor import WorkingDocumentFileAccessor


class LocalDocPusherService:
    """
    workフォルダの完成記事をdocumentフォルダに格納。手動＆自動(完成基準はタグ付与済みか)
    """

    def __init__(self, working_doc_file_accessor: WorkingDocumentFileAccessor):
        self.__working_doc_file_accessor = working_doc_file_accessor

    def push(self, title: str) -> Result[DocEntry, str]:
        doc_entry = self.__working_doc_file_accessor.move_to_store(title)
        return Result(doc_entry)

    def push_all(self):
        completed_work_filepaths = self.__working_doc_file_accessor.extract_completed_filepaths()
        results = []
        for file_path in completed_work_filepaths:
            result = self.push(file_path)
            results.append(result)
        return Results(*results)
