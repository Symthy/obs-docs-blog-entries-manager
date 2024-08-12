from domain.docs.datasource.interface import IDocumentMover, IWorkingDocumentReader
from domain.docs.entity.doc_entry import DocEntry


class LocalDocPusherService:
    """
    workフォルダの完成記事をdocumentフォルダに格納。手動＆自動(完成基準はタグ付与済みか)
    """

    def __init__(self, working_doc_file_accessor: IWorkingDocumentReader,
                 document_file_mover: IDocumentMover):
        self.__working_doc_file_accessor = working_doc_file_accessor
        self.__document_file_mover = document_file_mover

    def push(self, title: str):
        doc_entry = self.__working_doc_file_accessor.restore(title)
        self.__document_file_mover.move(self.__working_doc_file_accessor.build_file_path(title),
                                        doc_entry.doc_file_path)
        return doc_entry

    def push_all(self) -> list[DocEntry]:
        completed_work_filepaths = self.__working_doc_file_accessor.extract_completed_filepaths()
        doc_entries: list[DocEntry] = []
        for file_path in completed_work_filepaths:
            title = file_path.get_file_name()
            doc_entry = self.push(title)
            doc_entries.append(doc_entry)
        return doc_entries
