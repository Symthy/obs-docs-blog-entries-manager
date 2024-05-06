from __future__ import annotations

from domain.entries.interface import IEntryId


class PhotoEntryId(IEntryId):
    def __init__(self, entry_id: str):
        if not entry_id.isdigit():
            raise ValueError(f'Invalid photo entry ID: {entry_id}')
        self.__value = entry_id

    def new_instance(self, entry_id: str) -> PhotoEntryId:
        return PhotoEntryId(entry_id)

    @property
    def value(self) -> str:
        return self.__value

    def __eq__(self, other: PhotoEntryId):
        return self.__value == other.__value
