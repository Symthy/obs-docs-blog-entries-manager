from docs.entity.doc_entry import DocEntry
from entries.values.entry_date_time import EntryDateTime
from store.entity.stored_entry_list import StoredEntryList


class DocEntryIdBuilder:
    def __init__(self, stored_entry_list: StoredEntryList[DocEntry]):
        self.__stored_entry_list = stored_entry_list

    def build(self, current_date_time: EntryDateTime) -> str:
        # Todo
        return current_date_time.to_str_with_num_sequence()
