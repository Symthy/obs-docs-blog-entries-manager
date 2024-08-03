import files.file_system
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
    def __init__(self, store_dir_path: str):
        self.__store_dir_path = store_dir_path

    def build_for_blog(self) -> StoredBlogEntriesAccessor:
        entry_list_file_path = file_system.join_path(self.__store_dir_path, 'blog_entry_list.json')
        stored_blog_entry_dir_path = files.file_system.join_path(self.__store_dir_path, 'blog')
        stored_blog_entry_accessor = _StoredEntryAccessor(stored_blog_entry_dir_path, BlogEntryDeserializer())
        deserializer = StoredBlogEntryListDeserializer(entry_list_file_path)
        return StoredEntriesAccessor(entry_list_file_path, stored_blog_entry_accessor,
                                     deserializer.deserialize(), BlogEntries.new_instance)

    def build_for_doc(self) -> StoredDocEntriesAccessor:
        entry_list_file_path = file_system.join_path(self.__store_dir_path, 'doc_entry_list.json')
        stored_doc_entry_dir_path = files.file_system.join_path(self.__store_dir_path, 'doc')
        stored_doc_entry_accessor = _StoredEntryAccessor(stored_doc_entry_dir_path, DocEntryDeserializer())
        deserializer = StoredDocEntryListDeserializer(entry_list_file_path)
        return StoredEntriesAccessor(entry_list_file_path, stored_doc_entry_accessor,
                                     deserializer.deserialize(), DocEntries.new_instance)
