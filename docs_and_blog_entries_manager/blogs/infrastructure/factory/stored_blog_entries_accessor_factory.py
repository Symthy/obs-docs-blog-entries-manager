from blogs.domain.datasource.interface import StoredBlogEntriesAccessor
from blogs.domain.entity import BlogEntries
from blogs.domain.factory import BlogEntryDeserializer
from blogs.infrastructure.factory.stored_blog_entry_list_deserializer import StoredBlogEntryListDeserializer
from common.constants import LOCAL_STORE_DIR_PATH
from files.value import DirectoryPath, FilePath
from stores.infrastructure import StoredEntryAccessor, StoredEntriesAccessor


class StoredBlogEntriesAccessorFactory:
    def __init__(self, store_dir_path: DirectoryPath = LOCAL_STORE_DIR_PATH):
        self.__store_dir_path = store_dir_path

    def build(self) -> StoredBlogEntriesAccessor:
        entry_list_file_path: FilePath = self.__store_dir_path.add_file('blog_entry_list.json')
        stored_blog_entry_dir_path: DirectoryPath = self.__store_dir_path.add_dir('blog')
        stored_blog_entry_accessor = StoredEntryAccessor(stored_blog_entry_dir_path, BlogEntryDeserializer())
        deserializer = StoredBlogEntryListDeserializer(entry_list_file_path)
        return StoredEntriesAccessor(entry_list_file_path, stored_blog_entry_accessor,
                                     deserializer.deserialize(), BlogEntries.new_instance)
