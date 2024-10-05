from blogs.domain.entity import BlogEntries, BlogEntry
from blogs.domain.value import BlogEntryId
from blogs.infrastructure.types import StoredBlogEntryListHolder
from common.constants import BLOG_ENTRY_LIST_PATH
from files.value import FilePath
from stores.factory.stored_entry_list_deserializer import IStoredEntryListDeserializer, StoredEntryListDeserializer


class StoredBlogEntryListDeserializer(IStoredEntryListDeserializer[BlogEntries, BlogEntry, BlogEntryId]):
    def __init__(self, entry_list_file_path: FilePath = BLOG_ENTRY_LIST_PATH):
        self.__delegator = StoredEntryListDeserializer(BlogEntryId.new_instance, entry_list_file_path)

    def deserialize(self) -> StoredBlogEntryListHolder:
        return self.__delegator.deserialize()
