from __future__ import annotations

from entries.domain.interface import IEntryId
from entries.domain.value.entry_type import EntryType


class BlogEntryId(IEntryId):
    def __init__(self, entry_id: str):
        if not entry_id.isdigit():
            raise ValueError(f'Invalid blog entry ID: {entry_id}')
        self.__value = entry_id

    @classmethod
    def new_instance(cls, entry_id: str) -> BlogEntryId:
        return BlogEntryId(entry_id)

    @property
    def value(self) -> str:
        return self.__value

    @property
    def entry_type(self) -> EntryType:
        return EntryType.BLOG

    def __eq__(self, other: BlogEntryId):
        return self.__value == other.__value

    def __hash__(self):
        return hash(self.__value)

    def __str__(self):
        return self.__value
