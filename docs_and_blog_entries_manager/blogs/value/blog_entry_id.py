from __future__ import annotations

from entries.interface import IEntryId


class BlogEntryId(IEntryId):
    def __init__(self, entry_id: str):
        if not entry_id.isdigit():
            raise ValueError(f'Invalid blog entry ID: {entry_id}')
        self.__value = entry_id

    def new_instance(self, entry_id: str) -> BlogEntryId:
        return BlogEntryId(entry_id)

    @property
    def value(self) -> str:
        return self.__value

    def __eq__(self, other: BlogEntryId):
        return self.__value == other.__value
