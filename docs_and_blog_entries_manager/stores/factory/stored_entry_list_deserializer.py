from abc import ABC, abstractmethod
from typing import Generic, Callable

from blogs.domain.entity import BlogEntries, BlogEntry
from blogs.domain.value import BlogEntryId
from common.constants import BLOG_ENTRY_LIST_PATH, DOC_ENTRY_LIST_PATH
from docs.domain.entity import DocEntries, DocEntry
from docs.domain.value import DocEntryId
from entries.domain.interface import TI
from files import json_file
from files.value import FilePath
from stores.infrastructure import StoredEntryListHolder


class IStoredEntryListDeserializer(ABC):
    @abstractmethod
    def deserialize(self) -> StoredEntryListHolder:
        pass


class StoredBlogEntryListDeserializer(IStoredEntryListDeserializer):
    def __init__(self, entry_list_file_path: FilePath = BLOG_ENTRY_LIST_PATH):
        self.__delegator = StoredEntryListDeserializer(BlogEntryId.new_instance, entry_list_file_path)

    def deserialize(self) -> StoredEntryListHolder[BlogEntries, BlogEntry, BlogEntryId]:
        return self.__delegator.deserialize()


class StoredDocEntryListDeserializer(IStoredEntryListDeserializer):
    def __init__(self, entry_list_file_path: FilePath = DOC_ENTRY_LIST_PATH):
        self.__delegator = StoredEntryListDeserializer(DocEntryId.new_instance, entry_list_file_path)

    def deserialize(self) -> StoredEntryListHolder[DocEntries, DocEntry, DocEntryId]:
        return self.__delegator.deserialize()


class StoredEntryListDeserializer(IStoredEntryListDeserializer, Generic[TI]):
    def __init__(self, entry_id_builder: Callable[[str], TI], entry_list_file_path: FilePath):
        self.__entry_id_builder = entry_id_builder
        self.__entry_list_file_path = entry_list_file_path

    def deserialize(self) -> StoredEntryListHolder:
        stored_entry_list_json: dict[str: any] = json_file.load(self.__entry_list_file_path)
        return self.build(stored_entry_list_json)

    # Visible for Testing
    def build(self, stored_entry_list_json) -> StoredEntryListHolder:
        updated_at: str = stored_entry_list_json[StoredEntryListHolder.FIELD_UPDATED_AT] \
            if StoredEntryListHolder.FIELD_UPDATED_AT in stored_entry_list_json else ''
        entry_id_to_pickup_str: dict[str, str] = stored_entry_list_json[StoredEntryListHolder.FIELD_ENTRIES] \
            if StoredEntryListHolder.FIELD_ENTRIES in stored_entry_list_json else {}
        entry_id_to_pickup = {self.__entry_id_builder(eid): self.to_bool(pickup) for eid, pickup in
                              entry_id_to_pickup_str.items()}
        return StoredEntryListHolder(entry_id_to_pickup, updated_at)

    @staticmethod
    def to_bool(value: str) -> bool:
        return value == 'True'
