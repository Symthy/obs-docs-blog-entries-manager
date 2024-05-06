from typing import List

from domain.entries.values.category_path import CategoryPath
from domain.store.datasources.stored_entry_accessor import StoredEntryAccessor
from domain.store.entity.stored_entry_list import StoredEntryList
from domain.store.interface import IStoredEntriesAccessor, TM, TS, TI
from files import json_file


class StoredEntriesAccessor(IStoredEntriesAccessor[TM, TS, TI]):

    def __init__(self, entry_list_file_path: str, stored_entry_accessor: StoredEntryAccessor[TS, TI]):
        self.__entry_list_file_path = entry_list_file_path
        self.__stored_entry_accessor = stored_entry_accessor
        self.__stored_entry_list = StoredEntryList.deserialize(entry_list_file_path)

    def all_entries(self) -> List[TS]:
        return [self.__stored_entry_accessor.load_entry(entry_id) for entry_id in self.__stored_entry_list.entry_ids]

    def load_entries_by_ids(self, target_entry_ids: List[TI] = None) -> TM:
        entry_list = list(
            map(lambda entry_id: self.__stored_entry_accessor.load_entry(entry_id),
                filter(lambda entry_id: entry_id in self.__stored_entry_list.entry_ids, target_entry_ids)))
        return TM.new_instance(entry_list)

    def load_entries_by_category_path(self, category_path: CategoryPath) -> TM:
        entry_list: List[TS] = []
        for entry_id in self.__stored_entry_list.entry_ids:
            entry = self.__stored_entry_accessor.load_entry(entry_id)
            if entry.category_path == category_path:
                entry_list.append(entry)
            else:
                del entry  # 不要なインスタンスは即解放。メモリ節約
        return TM.new_instance(entry_list)

    def save_entries(self, entries: TM):
        for entry in entries.entry_list:
            self.__stored_entry_list.push_entry(entry)
            self.__stored_entry_accessor.save_entry(entry)
        json_file.save(self.__entry_list_file_path, self.__stored_entry_list.serialize())

    def load_entry(self, entry_id: TI) -> TS:
        return self.__stored_entry_accessor.load_entry(entry_id)

    def save_entry(self, entry: TS):
        self.__stored_entry_accessor.save_entry(entry)

    def search_entry_id(self, keyword: str) -> List[TI]:
        # Todo: specify other than title in keyword
        return self.__stored_entry_list.search_by_title(keyword)

    def has_entry(self, entry_id: TI) -> bool:
        return entry_id in self.__stored_entry_list.entry_ids
