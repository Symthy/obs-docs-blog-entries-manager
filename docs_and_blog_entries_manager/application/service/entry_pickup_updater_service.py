from typing import List

from domain.docs.value.doc_entry_id import DocEntryId
from infrastructure.store.composite.stored_both_entries_accessor import StoredBothEntriesAccessor


class EntryPickupUpdaterService:
    def __init__(self, stored_entries_accessor: StoredBothEntriesAccessor):
        self.__stored_entries_accessor = stored_entries_accessor

    def update_bulk(self, doc_entry_ids: List[DocEntryId], pickup: bool):
        for doc_entry_id in doc_entry_ids:
            self.update(doc_entry_id, pickup)

    def update(self, doc_id: DocEntryId, pickup: bool):
        self.__stored_entries_accessor.update_pickup(doc_id, pickup)
