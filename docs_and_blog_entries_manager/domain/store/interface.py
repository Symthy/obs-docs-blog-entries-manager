from abc import ABC
from typing import List, TypeVar, Generic

from domain.entries.interface import IEntryId, IEntry, IEntries
from domain.entries.values.category_path import CategoryPath

TM = TypeVar('TM', bound=IEntries)
TS = TypeVar('TS', bound=IEntry)
TI = TypeVar('TI', bound=IEntryId)


class IStoredEntryAccessor(ABC, Generic[TS, TI]):
    def load_entry(self, entry_id: TI) -> TS:
        pass

    def save_entry(self, entry: TI):
        pass


class IStoredEntriesAccessor(ABC, Generic[TM, TS, TI]):
    def load_entries(self) -> TM:
        pass

    def load_entries_by_id(self, entry_ids: List[TI] = None) -> TM:
        pass

    def load_entries_by_category_path(self, category_path: CategoryPath) -> TM:
        pass

    def save_entries(self, entries: TM):
        pass

    def search_entry_ids(self, keyword: str) -> List[TI]:
        pass

    def has_entry(self, entry_id: TI) -> bool:
        pass
