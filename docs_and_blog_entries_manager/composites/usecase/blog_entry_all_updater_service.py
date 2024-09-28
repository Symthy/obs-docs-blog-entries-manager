from blogs.domain.datasource.interface import StoredBlogEntriesAccessor
from blogs.domain.value import BlogEntryId
from composites.entity import BlogToDocEntryMapping
from composites.usecase import EntryToBlogPusherService, BlogEntryRemoverService
from docs.domain.datasource.interface import IDocumentReader, StoredDocEntriesAccessor
from docs.domain.entity import DocEntry
from docs.domain.value import DocEntryId


class BlogEntryAllUpdaterService:
    """
    投稿済みの記事で更新されたものがあればblogに投稿する
    新たにブログマーク(#Blog)が付与されたdocumentをblogに投稿する
    ブログマーク(#Blog)が消えたdocumentをblogから削除する
    """

    def __init__(self, stored_doc_entries_accessor: StoredDocEntriesAccessor,
                 stored_blog_entries_accessor: StoredBlogEntriesAccessor,
                 blog_entry_pusher: EntryToBlogPusherService,
                 blog_entry_remover: BlogEntryRemoverService,
                 blog_to_doc_mapping: BlogToDocEntryMapping,
                 document_reader: IDocumentReader):
        self.__stored_doc_entries_accessor = stored_doc_entries_accessor
        self.__stored_blog_entries_accessor = stored_blog_entries_accessor
        self.__blog_entry_pusher = blog_entry_pusher
        self.__blog_entry_remover = blog_entry_remover
        self.__blog_to_doc_mapping = blog_to_doc_mapping
        self.__document_reader = document_reader

    def execute(self):
        self.__update_blog_entries()
        self.__put_blog_entries()
        self.__remove_blog_entries()

    def __put_blog_entries(self):
        doc_entries_added_blog_category = self.__document_reader.extract_entries_with_blog_category()
        for doc_entry in doc_entries_added_blog_category.items:
            self.__blog_entry_pusher.execute(doc_entry.id)

    def __update_blog_entries(self):
        blog_to_doc: dict[BlogEntryId, DocEntryId] = self.__blog_to_doc_mapping.find_all()
        for blog_id, doc_id in blog_to_doc.items():
            blog_entry = self.__stored_blog_entries_accessor.load_entry(blog_id)
            doc_entry = self.__stored_doc_entries_accessor.load_entry(doc_id)
            if blog_entry.updated_at < doc_entry.updated_at:
                self.__blog_entry_pusher.execute(doc_entry.id)

    def __remove_blog_entries(self):
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
