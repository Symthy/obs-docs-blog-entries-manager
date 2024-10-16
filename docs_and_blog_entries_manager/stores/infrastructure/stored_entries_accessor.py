from typing import Callable

from entries.domain.interface import IStoredEntriesAccessor, TM, TI, TS
from entries.domain.value import CategoryPath
from files import json_file
from files.value import FilePath
from .interface import IStoredEntryListHolder
from .stored_entry_accessor import StoredEntryAccessor


class StoredEntriesAccessor(IStoredEntriesAccessor[TM, TS, TI]):

    def __init__(self, entry_list_file_path: FilePath, stored_entry_accessor: StoredEntryAccessor,
                 stored_entry_list: IStoredEntryListHolder, entries_builder: Callable[[list[TS]], TM]):
        self.__entry_list_file_path = entry_list_file_path
        self.__stored_entry_accessor = stored_entry_accessor
        self.__stored_entry_list: IStoredEntryListHolder = stored_entry_list
        self.__entries_builder = entries_builder

    def load_entry(self, entry_id: TI) -> TS:
        # delegate
        return self.__stored_entry_accessor.load_entry(entry_id)

    def load_entries(self) -> TM:
        # delegate
        return self.__entries_builder(
            [self.__stored_entry_accessor.load_entry(entry_id) for entry_id in self.__stored_entry_list.entry_ids])

    def load_entries_by_ids(self, target_entry_ids: list[TI] = None) -> TM:
        entry_list = list(
            map(lambda entry_id: self.__stored_entry_accessor.load_entry(entry_id),
                filter(lambda entry_id: entry_id in self.__stored_entry_list.entry_ids, target_entry_ids)))
        return self.__entries_builder(entry_list)

    def load_entries_by_category_path(self, category_path: CategoryPath) -> TM:
        # CategoryPath は容易に変更可能なためリストに保持しない。愚直に舐める。
        entry_list: list[TS] = []
        for entry_id in self.__stored_entry_list.entry_ids:
            # delegate
            entry = self.__stored_entry_accessor.load_entry(entry_id)
            if entry.category_path == category_path:
                entry_list.append(entry)
            else:
                del entry  # 不要なインスタンスは即解放。メモリ節約
        return self.__entries_builder(entry_list)

    def load_pickup_entries(self) -> TM:
        entries = list(map(lambda entry_id: self.load_entry(entry_id), self.__stored_entry_list.pickup_entry_ids))
        return self.__entries_builder(entries)

    def save_entry(self, entry: TS):
        # delegate
        return self.__stored_entry_accessor.save_entry(entry)

    def save_entries(self, entries: TM):
        for entry in entries.items:
            self.__stored_entry_list.push_entry(entry)
            self.__stored_entry_accessor.save_entry(entry)
        json_file.save(self.__entry_list_file_path, self.__stored_entry_list.serialize())

    def update_pickup(self, entry_id: TI, pickup: bool):
        self.__stored_entry_list.update_pickup(entry_id, pickup)
        self.__stored_entry_accessor.update_pickup(entry_id, pickup)

    def delete_entry(self, entry_id: TI):
        self.__stored_entry_accessor.delete_entry(entry_id)
        self.__stored_entry_list.delete_entry(entry_id)
