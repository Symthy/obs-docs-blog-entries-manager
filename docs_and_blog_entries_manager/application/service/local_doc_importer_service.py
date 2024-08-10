from domain.docs.datasources.interface import IDocumentAccessor
from domain.docs.entity.doc_entries import DocEntries
from infrastructure.types import StoredDocEntriesAccessor
from logs.logger import Logger


class LocalDocImporterService:
    """
    documentフォルダに直接作成された未登録記事を認識＆登録
    """

    def __init__(self, document_file_accessor: IDocumentAccessor,
                 stored_doc_entries_accessor: StoredDocEntriesAccessor):
        self.__document_file_accessor = document_file_accessor
        self.__stored_doc_entries_accessor = stored_doc_entries_accessor

    def execute(self):
        """
        内部保持のEntry一覧にあるか確認して、ないものは登録。記事にカテゴリ付与も行う
        """
        non_register_doc_entries: DocEntries = self.__document_file_accessor.extract_entries_with_non_register()
        if non_register_doc_entries.is_empty():
            Logger.info('Nothing new document.')
            return
        self.__stored_doc_entries_accessor.save_entries(non_register_doc_entries)
        for doc_entry in non_register_doc_entries.items:
            # Todo: 既に書かれていたら上書きする
            self.__document_file_accessor.insert_category_path(doc_entry.doc_file_path, doc_entry.category_path)
