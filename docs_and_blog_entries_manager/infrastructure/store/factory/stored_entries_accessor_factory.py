from domain.blogs.datasource.interface import StoredBlogEntriesAccessor
from domain.blogs.entity.blog_entries import BlogEntries
from domain.blogs.entity.factory.blog_entry_deserializer import BlogEntryDeserializer
from domain.docs.datasource.interface import StoredDocEntriesAccessor
from domain.docs.entity.doc_entries import DocEntries
from domain.docs.entity.factory.doc_entry_deserializer import DocEntryDeserializer
from files.value.file_path import DirectoryPath, FilePath
from infrastructure.store.factory.stored_entry_list_deserializer import StoredBlogEntryListDeserializer, \
    StoredDocEntryListDeserializer
from infrastructure.store.stored_entries_accessor import StoredEntriesAccessor
from infrastructure.store.stored_entry_accessor import _StoredEntryAccessor


class StoredEntriesAccessorFactory:
    def __init__(self, store_dir_path: DirectoryPath):
        self.__store_dir_path = store_dir_path

    def build_for_blog(self) -> StoredBlogEntriesAccessor:
        entry_list_file_path: FilePath = self.__store_dir_path.add_file('blog_entry_list.json')
        stored_blog_entry_dir_path: DirectoryPath = self.__store_dir_path.add_dir('blog')
        stored_blog_entry_accessor = _StoredEntryAccessor(stored_blog_entry_dir_path, BlogEntryDeserializer())
        deserializer = StoredBlogEntryListDeserializer(entry_list_file_path)
        return StoredEntriesAccessor(entry_list_file_path, stored_blog_entry_accessor,
                                     deserializer.deserialize(), BlogEntries.new_instance)

    def build_for_doc(self) -> StoredDocEntriesAccessor:
        entry_list_file_path = self.__store_dir_path.add_file('doc_entry_list.json')
        stored_doc_entry_dir_path = self.__store_dir_path.add_dir('doc')
        stored_doc_entry_accessor = _StoredEntryAccessor(stored_doc_entry_dir_path, DocEntryDeserializer())
        deserializer = StoredDocEntryListDeserializer(entry_list_file_path)
        return StoredEntriesAccessor(entry_list_file_path, stored_doc_entry_accessor,
                                     deserializer.deserialize(), DocEntries.new_instance)
