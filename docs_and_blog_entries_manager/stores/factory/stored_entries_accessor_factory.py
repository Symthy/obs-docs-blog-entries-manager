from blogs.domain.datasource.interface import StoredBlogEntriesAccessor
from blogs.domain.entity.blog_entries import BlogEntries
from blogs.domain.factory import BlogEntryDeserializer
from docs.domain.datasource.interface import StoredDocEntriesAccessor
from docs.domain.entity import DocEntries
from docs.domain.factory import DocEntryDeserializer
from files.value import (DirectoryPath, FilePath)
from stores.factory import StoredBlogEntryListDeserializer, StoredDocEntryListDeserializer
from stores.infrastructure import StoredEntriesAccessor
from stores.infrastructure import StoredEntryAccessor


class StoredEntriesAccessorFactory:
    def __init__(self, store_dir_path: DirectoryPath):
        self.__store_dir_path = store_dir_path

    def build_for_blog(self) -> StoredBlogEntriesAccessor:
        entry_list_file_path: FilePath = self.__store_dir_path.add_file('blog_entry_list.json')
        stored_blog_entry_dir_path: DirectoryPath = self.__store_dir_path.add_dir('blog')
        stored_blog_entry_accessor = StoredEntryAccessor(stored_blog_entry_dir_path, BlogEntryDeserializer())
        deserializer = StoredBlogEntryListDeserializer(entry_list_file_path)
        return StoredEntriesAccessor(entry_list_file_path, stored_blog_entry_accessor,
                                     deserializer.deserialize(), BlogEntries.new_instance)

    def build_for_doc(self) -> StoredDocEntriesAccessor:
        entry_list_file_path = self.__store_dir_path.add_file('doc_entry_list.json')
        stored_doc_entry_dir_path = self.__store_dir_path.add_dir('doc')
        stored_doc_entry_accessor = StoredEntryAccessor(stored_doc_entry_dir_path, DocEntryDeserializer())
        deserializer = StoredDocEntryListDeserializer(entry_list_file_path)
        return StoredEntriesAccessor(entry_list_file_path, stored_doc_entry_accessor,
                                     deserializer.deserialize(), DocEntries.new_instance)
