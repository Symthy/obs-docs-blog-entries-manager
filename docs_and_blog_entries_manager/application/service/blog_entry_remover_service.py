from common.constants import BLOG_CATEGORY
from domain.blogs.datasource.interface import IBlogEntryModifier, StoredBlogEntriesAccessor
from domain.docs.datasource.interface import IDocumentModifier
from domain.docs.value.doc_entry_id import DocEntryId
from domain.mappings.blog_to_doc_entry_mapping import BlogToDocEntryMapping


class BlogEntryRemoverService:
    """
    指定したdocumentに対応するblogの記事を削除する
    """

    def __init__(self, document_file_modifier: IDocumentModifier,
                 blog_entry_modifier: IBlogEntryModifier,
                 blog_to_doc_entry_mapping: BlogToDocEntryMapping,
                 stored_blog_entries_accessor: StoredBlogEntriesAccessor):
        self.__document_file_modifier = document_file_modifier
        self.__blog_entry_modifier = blog_entry_modifier
        self.__blog_to_doc_entry_mapping = blog_to_doc_entry_mapping
        self.__stored_blog_entries_accessor = stored_blog_entries_accessor

    def execute(self, doc_id: DocEntryId):
        self.__document_file_modifier.delete_category(doc_id, BLOG_CATEGORY)
        blog_entry_id = self.__blog_to_doc_entry_mapping.find_blog_entry_id(doc_id)
        self.__blog_entry_modifier.delete(blog_entry_id)
        self.__stored_blog_entries_accessor.delete_entry(blog_entry_id)
