from __future__ import annotations

from typing import Dict, List, Any, Generic

from domain.entries.interface import TM, TS, TI
from files import json_file
from ltimes import datetime_functions


class StoredEntryListHolder(Generic[TM, TS, TI]):
    """
    xxx_entry_list.jsonの全データを保持するクラス
    """
    FIELD_UPDATED_AT = 'updated_at'
    FIELD_ENTRIES = 'entries'

    def __init__(self, entry_id_to_title: Dict[TI, str], updated_at: str):
        self.__entry_id_to_title = entry_id_to_title
        self.__updated_at = updated_at

    @property
    def entry_ids(self) -> List[TI]:
        return list(self.__entry_id_to_title.keys())

    def push_entry(self, entry: TS):
        self.__entry_id_to_title[entry.id] = entry.title

    def push_entries(self, entries: TM):
        for entry in entries.items:
            self.push_entry(entry)

    def exist_id(self, entry_id: TI) -> bool:
        return entry_id in self.__entry_id_to_title.keys()

    def search_by_title(self, keyword: str) -> List[TI]:
        entry_ids = [eid for eid, title in self.__entry_id_to_title.items() if keyword.lower() in title.lower()]
        return entry_ids

    def serialize(self) -> Dict[str, Any]:
        return {
            StoredEntryListHolder.FIELD_UPDATED_AT: datetime_functions.current_datetime(),
            StoredEntryListHolder.FIELD_ENTRIES: {eid.value: title for eid, title in self.__entry_id_to_title}
        }

    @staticmethod
    def deserialize(entry_list_file_path: str) -> StoredEntryListHolder:
        stored_entry_list_json: dict[str: any] = json_file.load(entry_list_file_path)
        updated_at: str = stored_entry_list_json[StoredEntryListHolder.FIELD_UPDATED_AT] \
            if StoredEntryListHolder.FIELD_UPDATED_AT in stored_entry_list_json else ''
        entry_id_to_tile: dict[str, str] = stored_entry_list_json[StoredEntryListHolder.FIELD_ENTRIES] \
            if StoredEntryListHolder.FIELD_ENTRIES in stored_entry_list_json else {}
        entry_id_to_title: Dict[TI, str] = {TI.new_instance(eid): title for eid, title in entry_id_to_tile}
        return StoredEntryListHolder(entry_id_to_title, updated_at)

# json data format
# {
#   "updated_at": "2022-01-02T03:04:05+0900",
#   "entries": {
#     "id": "title"
#      :
#   }
# }
