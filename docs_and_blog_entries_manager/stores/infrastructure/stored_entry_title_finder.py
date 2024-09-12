from typing import Generic

from entries.domain.interface import TS, TM
from stores.infrastructure.stored_entries_accessor import StoredEntriesAccessor


class StoredEntryTitleFinder(Generic[TS]):
    def __init__(self, stored_entries_accessor: StoredEntriesAccessor):
        self.__accessor = stored_entries_accessor

    def find(self, title: str) -> TS | None:
        entries: TM = self.__accessor.load_entries()
        return entries.find_by_title(title)
