from domain.blogs.entity.blog_entry import BlogEntry
from domain.docs.entity.doc_entry import DocEntry
from infrastructure.store.blog_to_doc_entry_mapping import BlogToDocEntryMapping
from infrastructure.types import StoredDocEntriesAccessor, StoredBlogEntriesAccessor


class EntryPersistenceService:
    def __init__(self, doc_entries_accessor: StoredDocEntriesAccessor, blog_entries_accessor: StoredBlogEntriesAccessor,
                 entry_mapping: BlogToDocEntryMapping):
        self.__doc_entries_accessor = doc_entries_accessor
        self.__blog_entries_accessor = blog_entries_accessor
        self.__entry_mapping = entry_mapping

    def save_entry_data(self, blog_entry: BlogEntry, doc_entry: DocEntry):
        self.__doc_entries_accessor.save_entry(doc_entry)
        self.__blog_entries_accessor.save_entry(blog_entry)
        self.__entry_mapping.push_entry_pair(blog_entry.id, doc_entry.id)
