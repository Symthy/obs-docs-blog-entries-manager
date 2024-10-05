from docs.domain.datasource.interface import IDocDocumentAccessor, StoredDocEntriesModifier
from docs.domain.entity import DocEntries
from logs.logger import Logger


class LocalDocImporterService:
    """
    documentフォルダに直接作成された未登録記事を認識＆登録
    """

    def __init__(self, document_file_accessor: IDocDocumentAccessor,
                 stored_doc_entries_modifier: StoredDocEntriesModifier):
        self.__document_file_accessor = document_file_accessor
        self.__stored_doc_entries_modifier = stored_doc_entries_modifier

    def execute(self):
        """
        内部保持のEntry一覧にあるか確認して、ないものは登録。記事にカテゴリ付与も行う
        """
        non_register_doc_entries: DocEntries = self.__document_file_accessor.extract_entries_with_non_register()
        if non_register_doc_entries.is_empty():
            Logger.info('Nothing new document.')
            return
        self.__stored_doc_entries_modifier.save_entries(non_register_doc_entries)
        for doc_entry in non_register_doc_entries.items:
            self.__document_file_accessor.insert_category_path_to_content(doc_entry.doc_file_path,
                                                                          doc_entry.category_path)
