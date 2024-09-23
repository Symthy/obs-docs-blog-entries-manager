from __future__ import annotations

from typing import Generic

from entries.domain.interface import TM, TS, TI
from ltimes import datetime_functions


# Todo: Generics -> interface
class StoredEntryListHolder(Generic[TM, TS, TI]):
    """
    xxx_entry_list.jsonの全データを保持するための共通クラス
    """
    FIELD_UPDATED_AT = 'updated_at'
    FIELD_ENTRIES = 'entries'

    def __init__(self, entry_id_to_pickup: dict[TI, bool], updated_at: str):
        self.__entry_id_to_pickup = entry_id_to_pickup
        self.__updated_at = updated_at

    @property
    def entry_ids(self) -> list[TI]:
        return list(self.__entry_id_to_pickup.keys())

    @property
    def pickup_entry_ids(self) -> list[TI]:
        return [entry_id for entry_id, pickup in self.__entry_id_to_pickup if pickup is True]

    @property
    def update_at(self) -> str:
        return self.__updated_at

    def push_entry(self, entry: TS):
        self.__entry_id_to_pickup[entry.id.value] = entry.pickup

    def push_entries(self, entries: TM):
        for entry in entries.items:
            self.push_entry(entry)

    def update_pickup(self, entry_id: TI, pickup: bool):
        self.__entry_id_to_pickup[entry_id] = pickup

    def delete_entry(self, entry_id: TI):
        self.__entry_id_to_pickup.pop(entry_id)

    def exist_id(self, entry_id: TI) -> bool:
        return entry_id in self.__entry_id_to_pickup

    def is_pickup(self, entry_id: TI) -> bool:
        if not self.exist_id:
            return False
        return self.__entry_id_to_pickup[entry_id]

    def serialize(self) -> dict[str, dict[str, bool]]:
        return {
            StoredEntryListHolder.FIELD_UPDATED_AT: datetime_functions.current_datetime(),
            StoredEntryListHolder.FIELD_ENTRIES: {eid.value: pickup for eid, pickup in self.__entry_id_to_pickup}
        }

# json data format
# {
#   "updated_at": "2022-01-02T03:04:05+0900",
#   "entries": [
#     "entry_id": false
#      :
#   ]
# }
