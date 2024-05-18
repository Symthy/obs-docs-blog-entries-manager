from typing import List

from application.service.summary_entry_pusher_service import SummaryEntryPusherService
from domain.docs.value.doc_entry_id import DocEntryId
from infrastructure.store.composite.stored_both_entries_accessor import StoredBothEntriesAccessor


class EntryPickupUpdaterService:
    def __init__(self, stored_entries_accessor: StoredBothEntriesAccessor,
                 summary_entry_pusher: SummaryEntryPusherService):
        self.__stored_entries_accessor = stored_entries_accessor
        self.__summary_entry_pusher = summary_entry_pusher

    def update_bulk(self, doc_entry_ids: List[DocEntryId], pickup: bool):
        for doc_entry_id in doc_entry_ids:
            self.__stored_entries_accessor.update_pickup(doc_entry_id, pickup)
        self.__summary_entry_pusher.push_bulk()

    def update(self, doc_id: DocEntryId, pickup: bool):
        self.__stored_entries_accessor.update_pickup(doc_id, pickup)
        self.__summary_entry_pusher.push_bulk()
