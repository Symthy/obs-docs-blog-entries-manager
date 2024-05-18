from domain.docs.value.doc_entry_id import DocEntryId
from infrastructure.store.blog_to_doc_entry_mapping import BlogToDocEntryMapping
from infrastructure.types import StoredBlogEntriesAccessor, StoredDocEntriesAccessor


class StoredBothEntriesAccessor:
    def __init__(self, stored_blog_entry_accessor: StoredBlogEntriesAccessor,
                 stored_doc_entry_accessor: StoredDocEntriesAccessor,
                 blog_to_doc_entry_mapping: BlogToDocEntryMapping):
        self.__stored_blog_entry_accessor = stored_blog_entry_accessor
        self.__stored_doc_entry_accessor = stored_doc_entry_accessor
        self.__blog_to_doc_entry_mapping = blog_to_doc_entry_mapping

    def update_pickup(self, doc_entry_id: DocEntryId, pickup: bool):
        self.__stored_doc_entry_accessor.update_pickup(doc_entry_id, pickup)
        blog_entry_id = self.__blog_to_doc_entry_mapping.find_blog_entry_id(doc_entry_id)
        self.__stored_blog_entry_accessor.update_pickup(blog_entry_id, pickup)
