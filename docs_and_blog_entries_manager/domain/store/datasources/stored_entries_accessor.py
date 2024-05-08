from typing import List, Callable

from domain.entries.values.category_path import CategoryPath
from domain.store.entity.stored_entry_list import StoredEntryList
from domain.store.interface import IStoredEntriesAccessor, IStoredEntryAccessor, TM, TI, TS
from files import json_file


class StoredEntriesAccessor(IStoredEntriesAccessor[TM, TS, TI]):

    def __init__(self, entry_list_file_path: str, stored_entry_accessor: IStoredEntryAccessor,
                 entries_builder: Callable[[List[TS]], TM]):
        self.__entry_list_file_path = entry_list_file_path
        self.__stored_entry_accessor = stored_entry_accessor
        self.__stored_entry_list = StoredEntryList.deserialize(entry_list_file_path)
        self.__entries_builder = entries_builder

    def load_entries(self) -> TM:
        return self.__entries_builder(
            [self.__stored_entry_accessor.load_entry(entry_id) for entry_id in self.__stored_entry_list.entry_ids])

    def load_entries_by_id(self, target_entry_ids: List[TI] = None) -> TM:
        entry_list = list(
            map(lambda entry_id: self.__stored_entry_accessor.load_entry(entry_id),
                filter(lambda entry_id: entry_id in self.__stored_entry_list.entry_ids, target_entry_ids)))
        return self.__entries_builder(entry_list)

    def load_entries_by_category_path(self, category_path: CategoryPath) -> TM:
        entry_list: List[TS] = []
        for entry_id in self.__stored_entry_list.entry_ids:
            entry = self.__stored_entry_accessor.load_entry(entry_id)
            if entry.category_path == category_path:
                entry_list.append(entry)
            else:
                del entry  # 不要なインスタンスは即解放。メモリ節約
        return self.__entries_builder(entry_list)

    def save_entries(self, entries: TM):
        for entry in entries.items:
            self.__stored_entry_list.push_entry(entry)
            self.__stored_entry_accessor.save_entry(entry)
        json_file.save(self.__entry_list_file_path, self.__stored_entry_list.serialize())

    def search_entry_id(self, keyword: str) -> List[TI]:
        # Todo: specify other than title in keyword
        return self.__stored_entry_list.search_by_title(keyword)

    def has_entry(self, entry_id: TI) -> bool:
        return entry_id in self.__stored_entry_list.entry_ids
