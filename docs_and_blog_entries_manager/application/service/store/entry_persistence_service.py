from domain.blogs.entity.blog_entry import BlogEntry
from domain.docs.entity.doc_entry import DocEntry
from domain.docs.value.doc_entry_id import DocEntryId


class EntryPersistenceService:
    def __init__(self, doc_entry_accessor, blog_entry_accessor, entry_mapping):
        self.__doc_entry_accessor = doc_entry_accessor
        self.__blog_entry_accessor = blog_entry_accessor
        self.__entry_mapping = entry_mapping

    def save_entry_data(self, blog_entry: BlogEntry, doc_entry: DocEntry):
        self.__doc_entry_accessor.save_entry(doc_entry)
        self.__blog_entry_accessor.save_entry(blog_entry)
        self.__entry_mapping.push_entry_pair(blog_entry.id, doc_entry.id)

    def save_blog_entry(self, blog_entry: BlogEntry, doc_entry_id: DocEntryId):
        self.__blog_entry_accessor.save_entry(blog_entry)
        self.__entry_mapping.push_entry_pair(blog_entry.id, doc_entry_id)
