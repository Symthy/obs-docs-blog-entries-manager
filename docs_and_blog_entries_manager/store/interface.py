from abc import ABC
from typing import TypeVar, Generic, List

from blogs.entity.blog_entries import BlogEntries
from blogs.entity.blog_entry import BlogEntry
from blogs.value.blog_entry_id import BlogEntryId
from docs.entity.doc_entries import DocEntries
from docs.entity.doc_entry import DocEntry
from docs.value.doc_entry_id import DocEntryId

TM = TypeVar('TM', DocEntries, BlogEntries)
TS = TypeVar('TS', DocEntry, BlogEntry)
TI = TypeVar('TI', DocEntryId, BlogEntryId)


class IStoredEntryAccessor(ABC, Generic[TS, TI]):
    def load_entry(self, entry_id: TI) -> TS:
        pass

    def save_entry(self, entry: TS):
        pass


class IStoredEntriesAccessor(IStoredEntryAccessor[TS, TI], Generic[TM, TS, TI]):
    def load_entries(self, entry_ids: List[TI] = None) -> TM:
        pass

    def save_entries(self, entries: TM):
        pass

    def load_entry(self, entry_id: TI) -> TS:
        pass

    def save_entry(self, entry: TS):
        pass

    def search_entry_ids(self, keyword: str) -> List[TI]:
        pass

    def has_entry(self, entry_id: TI) -> bool:
        pass
