from application.service.blog_entry_pusher_service import BlogEntryPusherService
from application.service.blog_entry_remover_service import BlogEntryRemoverService
from common.results import Results
from domain.docs.datasources.interface import IDocumentFileReader
from domain.docs.entity.doc_entry import DocEntry
from infrastructure.types import StoredDocEntriesAccessor


class BlogEntryAllUpdaterService:
    """
    新たにブログマーク(#Blog)が付与されたdocumentをblogに投稿する
    ブログマーク(#Blog)が消えたdocumentをblogから削除する
    """

    def __init__(self, stored_doc_entries_accessor: StoredDocEntriesAccessor,
                 blog_entry_pusher: BlogEntryPusherService, blog_entry_remover: BlogEntryRemoverService,
                 document_reader: IDocumentFileReader):
        self.__stored_doc_entries_accessor = stored_doc_entries_accessor
        self.__blog_entry_pusher = blog_entry_pusher
        self.__blog_entry_remover = blog_entry_remover
        self.__document_reader = document_reader

    def execute(self):
        results = self.__post_blog_entries()
        return results.merge(self.__remove_blog_entries())

    def __post_blog_entries(self):
        results = []
        doc_entries_added_blog_category = self.__document_reader.extract_entries_with_blog_category()
        for doc_entry in doc_entries_added_blog_category.items:
            result = self.__blog_entry_pusher.execute(doc_entry.id)
            results.append(result)
        return Results(*results)

    def __remove_blog_entries(self):
        results = []
        doc_entries_has_blog_category: list[DocEntry] \
            = self.__stored_doc_entries_accessor.load_entries().items_filtered_blog_category()
        for old_doc_entry in doc_entries_has_blog_category:
            current_doc_entry = self.__document_reader.restore(old_doc_entry.doc_file_path)
            if old_doc_entry.equals_updated_at(current_doc_entry):
                continue
            if current_doc_entry.contains_blog_category():
                continue
            self.__stored_doc_entries_accessor.save_entry(current_doc_entry)
            self.__blog_entry_remover.execute(current_doc_entry.id)
        return Results(*results)  # Todo
