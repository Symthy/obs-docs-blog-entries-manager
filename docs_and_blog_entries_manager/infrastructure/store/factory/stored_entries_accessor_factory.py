from domain.blogs.entity.blog_entries import BlogEntries
from domain.blogs.entity.factory.blog_entry_deserializer import BlogEntryDeserializer
from domain.docs.entity.doc_entries import DocEntries
from domain.docs.entity.factory.doc_entry_deserializer import DocEntryDeserializer
from files import file_system
from infrastructure.store.factory.stored_entry_list_deserializer import StoredBlogEntryListDeserializer, \
    StoredDocEntryListDeserializer
from infrastructure.store.stored_entries_accessor import StoredEntriesAccessor
from infrastructure.store.stored_entry_accessor import _StoredEntryAccessor
from infrastructure.types import StoredBlogEntriesAccessor, StoredDocEntriesAccessor


class StoredEntriesAccessorFactory:
    def __init__(self, stored_entry_dir_path: str):
        self.__stored_entry_dir_path = stored_entry_dir_path

    def build_for_blog(self) -> StoredBlogEntriesAccessor:
        entry_list_file_path = file_system.join_path(self.__stored_entry_dir_path, 'blog_entry_list.json')
        stored_blog_entry_accessor = _StoredEntryAccessor(self.__stored_entry_dir_path, BlogEntryDeserializer())
        return StoredEntriesAccessor(entry_list_file_path, stored_blog_entry_accessor,
                                     StoredBlogEntryListDeserializer(), BlogEntries.new_instance)

    def build_for_doc(self) -> StoredDocEntriesAccessor:
        entry_list_file_path = file_system.join_path(self.__stored_entry_dir_path, 'doc_entry_list.json')
        stored_doc_entry_accessor = _StoredEntryAccessor(self.__stored_entry_dir_path, DocEntryDeserializer())
        return StoredEntriesAccessor(entry_list_file_path, stored_doc_entry_accessor,
                                     StoredDocEntryListDeserializer(), DocEntries.new_instance)
