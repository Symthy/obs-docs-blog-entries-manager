from domain.entries.interface import TS, TM
from infrastructure.store.stored_entries_accessor import StoredEntriesAccessor


class StoredEntryTitleFinder:
    def __init__(self, stored_entries_accessor: StoredEntriesAccessor):
        self.__accessor = stored_entries_accessor

    def find(self, title) -> TS | None:
        entries: TM = self.__accessor.load_entries()
        return entries.find_by_title(title)
