from abc import ABC
from typing import TypeVar, Generic, List

from domain.blogs.entity.blog_entries import BlogEntries
from domain.blogs.entity.blog_entry import BlogEntry
from domain.blogs.value import BlogEntryId
from domain.docs import DocEntry
from domain.docs.entity.doc_entries import DocEntries
from domain.docs.value import DocEntryId

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
