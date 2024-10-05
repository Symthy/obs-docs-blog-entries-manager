from abc import ABC, abstractmethod
from typing import Generic, Callable

from entries.domain.interface import TI, TM, TS
from files import json_file
from files.value import FilePath
from stores.infrastructure import StoredEntryListHolder


class IStoredEntryListDeserializer(ABC, Generic[TM, TS, TI]):
    @abstractmethod
    def deserialize(self) -> StoredEntryListHolder:
        pass


class StoredEntryListDeserializer(IStoredEntryListDeserializer):
    def __init__(self, entry_id_builder: Callable[[str], TI], entry_list_file_path: FilePath = None):
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
