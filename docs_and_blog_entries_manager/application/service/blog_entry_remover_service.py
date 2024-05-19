from domain.docs.value.doc_entry_id import DocEntryId
from infrastructure.documents.document_file_accessor import DocumentFileAccessor
from infrastructure.hatena.blog_entry_repository import BlogEntryRepository
from infrastructure.store.blog_to_doc_entry_mapping import BlogToDocEntryMapping
from infrastructure.types import StoredBlogEntriesAccessor


class BlogEntryRemoverService:
    """
    指定したdocumentに対応するblogの記事を削除する
    """

    def __init__(self, document_file_accessor: DocumentFileAccessor, blog_entry_repository: BlogEntryRepository,
                 blog_to_doc_entry_mapping: BlogToDocEntryMapping,
                 stored_blog_entries_accessor: StoredBlogEntriesAccessor):
        self.__document_file_accessor = document_file_accessor
        self.__blog_entry_repository = blog_entry_repository
        self.__blog_to_doc_entry_mapping = blog_to_doc_entry_mapping
        self.__stored_blog_entries_accessor = stored_blog_entries_accessor

    def execute(self, doc_id: DocEntryId):
        self.__document_file_accessor.remove_blog_category(doc_id)
        blog_entry_id = self.__blog_to_doc_entry_mapping.find_blog_entry_id(doc_id)
        self.__blog_entry_repository.delete(blog_entry_id)
        self.__stored_blog_entries_accessor.delete_entry(blog_entry_id)
