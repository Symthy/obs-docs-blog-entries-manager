from abc import ABC
from typing import TypeVar, Generic, Optional, List

from blogs.entity.blog_entries import BlogEntries
from blogs.entity.blog_entry import BlogEntry
from docs.entity.doc_entries import DocEntries
from docs.entity.doc_entry import DocEntry

TM = TypeVar('TM', DocEntries, BlogEntries)
TS = TypeVar('TS', DocEntry, BlogEntry)


class IStoredEntryAccessor(ABC, Generic[TS]):
    def load_entry(self, entry_id: str) -> TS:
        pass

    def save_entry(self, entry: TS):
        pass


class IStoredEntriesAccessor(IStoredEntryAccessor[TS], Generic[TM, TS]):
    def load_entries(self, entry_ids: Optional[List[str]] = None) -> TM:
        pass

    def save_entries(self, entries: TM):
        pass

    def load_entry(self, entry_id: str) -> TS:
        pass

    def save_entry(self, entry: TS):
        pass

    def search_entry_ids(self, keyword: str) -> List[str]:
        pass

    def has_entry(self, entry_id: str) -> bool:
        pass
