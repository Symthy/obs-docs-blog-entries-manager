from __future__ import annotations

from datetime import datetime

from domain.entries.interface import IEntryId
from domain.entries.values.entry_date_time import EntryDateTime


class DocEntryId(IEntryId):
    def __init__(self, entry_id: str | datetime):
        eid: str = EntryDateTime(entry_id).to_str_with_num_sequence() if isinstance(entry_id, datetime) else entry_id
        if not eid.isdigit() and len(entry_id) != 17:
            raise ValueError(f'Invalid doc entry ID: {eid}')
        self.__value = eid
        # example: 20240505010203000

    def new_instance(self, entry_id: str) -> DocEntryId:
        return DocEntryId(entry_id)

    @property
    def value(self) -> str:
        return self.__value

    def __eq__(self, other: DocEntryId):
        return self.__value == other.__value

    def __hash__(self):
        return hash(self.__value)

    @staticmethod
    def build(current_date_time: EntryDateTime = EntryDateTime()) -> DocEntryId:
        # 時刻のミリ秒までをIDにする（重複回避）
        return DocEntryId(current_date_time.to_str_with_num_sequence()[:-3])
