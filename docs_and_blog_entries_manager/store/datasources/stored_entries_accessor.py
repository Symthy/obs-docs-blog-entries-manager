from typing import List

from files import json_file
from store.datasources.stored_entry_accessor import StoredEntryAccessor
from store.entity.stored_entry_list import StoredEntryList
from store.interface import IStoredEntriesAccessor, TM, TS


class StoredEntriesAccessor(IStoredEntriesAccessor[TM, TS]):

    def __init__(self, entry_list_file_path: str, stored_entry_accessor: StoredEntryAccessor[TS]):
        self.__entry_list_file_path = entry_list_file_path
        self.__stored_entry_accessor = stored_entry_accessor
        self.__stored_entry_list = StoredEntryList(entry_list_file_path, stored_entry_accessor)

    def load_entries(self, target_entry_ids: List[str] = None) -> TM:
        entries = TM.new_instance(self.__stored_entry_list.convert_entries(target_entry_ids))
        return entries

    def save_entries(self, entries: TM):
        for entry in entries.entry_list:
            self.__stored_entry_list.push_entry(entry)
            self.__stored_entry_accessor.save_entry(entry)
        json_file.save(self.__entry_list_file_path, self.__stored_entry_list.serialize())

    def load_entry(self, entry_id: str) -> TS:
        return self.__stored_entry_accessor.load_entry(entry_id)

    def save_entry(self, entry: TS):
        self.__stored_entry_accessor.save_entry(entry)

    def search_entry_id(self, keyword: str) -> List[str]:
        # Todo: specify other than title in keyword
        return self.__stored_entry_list.search_by_title(keyword)

    def has_entry(self, entry_id) -> bool:
        return entry_id in self.__stored_entry_list.entry_ids
