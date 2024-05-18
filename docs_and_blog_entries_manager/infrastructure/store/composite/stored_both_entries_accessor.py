from domain.blogs.entity.blog_entry import BlogEntry
from domain.docs.entity.doc_entry import DocEntry
from domain.docs.value.doc_entry_id import DocEntryId
from infrastructure.store.blog_to_doc_entry_mapping import BlogToDocEntryMapping
from infrastructure.types import StoredBlogEntriesAccessor, StoredDocEntriesAccessor


class StoredBothEntriesAccessor:
    def __init__(self, stored_blog_entries_accessor: StoredBlogEntriesAccessor,
                 stored_doc_entries_accessor: StoredDocEntriesAccessor,
                 blog_to_doc_entry_mapping: BlogToDocEntryMapping):
        self.__stored_blog_entries_accessor = stored_blog_entries_accessor
        self.__stored_doc_entries_accessor = stored_doc_entries_accessor
        self.__blog_to_doc_entry_mapping = blog_to_doc_entry_mapping

    def save_entry(self, blog_entry: BlogEntry, doc_entry: DocEntry):
        self.__stored_doc_entries_accessor.save_entry(doc_entry)
        self.__stored_blog_entries_accessor.save_entry(blog_entry)
        self.__blog_to_doc_entry_mapping.push_entry_pair(blog_entry.id, doc_entry.id)

    def update_pickup(self, doc_entry_id: DocEntryId, pickup: bool):
        self.__stored_doc_entries_accessor.update_pickup(doc_entry_id, pickup)
        blog_entry_id = self.__blog_to_doc_entry_mapping.find_blog_entry_id(doc_entry_id)
        self.__stored_blog_entries_accessor.update_pickup(blog_entry_id, pickup)
