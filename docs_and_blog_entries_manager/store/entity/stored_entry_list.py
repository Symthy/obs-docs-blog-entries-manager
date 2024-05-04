from __future__ import annotations

from typing import Dict, List, Any, Generic

from files import json_file
from ltimes import datetime_functions
from store.interface import TM, TS


class StoredEntryList(Generic[TM, TS]):
    """
    xxx_entry_list.jsonの全データを保持するクラス
    """
    FIELD_UPDATED_TIME = 'updated_time'
    FIELD_ENTRIES = 'entries'

    def __init__(self, entry_list_file_path: str):
        stored_entry_list = json_file.load(entry_list_file_path)
        self.__updated_time: str = stored_entry_list[StoredEntryList.FIELD_UPDATED_TIME] \
            if StoredEntryList.FIELD_UPDATED_TIME in stored_entry_list else ''
        self.__entry_id_to_title: Dict[str, str] = stored_entry_list[StoredEntryList.FIELD_ENTRIES] \
            if StoredEntryList.FIELD_ENTRIES in stored_entry_list else {}

    @property
    def entry_ids(self) -> List[str]:
        return list(self.__entry_id_to_title.keys())

    def push_entry(self, entry: TS):
        self.__entry_id_to_title[entry.id] = entry.title

    def search_by_title(self, keyword: str) -> List[str]:
        entry_ids = [eid for eid, title in self.__entry_id_to_title.items() if keyword.lower() in title.lower()]
        return entry_ids

    def serialize(self) -> Dict[str, Any]:
        return {
            StoredEntryList.FIELD_UPDATED_TIME: datetime_functions.current_datetime(),
            StoredEntryList.FIELD_ENTRIES: self.__entry_id_to_title
        }

# json data format
# {
#   "updated_time": "2022-01-02T03:04:05",
#   "entries": {
#     "id": "title"
#      :
#   }
# }
