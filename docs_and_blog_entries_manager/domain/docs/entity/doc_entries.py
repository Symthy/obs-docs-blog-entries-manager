from __future__ import annotations

from typing import List, Optional

from domain.docs.entity.doc_entry import DocEntry
from domain.docs.value.doc_entry_id import DocEntryId
from domain.entries.interface import IEntries


class DocEntries(IEntries):
    def __init__(self, entries: List[DocEntry] = None):
        self.__entries: dict[str, DocEntry] = {}
        if entries is not None:
            self.__entries = {entry.id: entry for entry in entries}

    @property
    def items(self) -> list[DocEntry]:
        return list(self.__entries.values())

    def items_filtered_blog_category(self) -> list[DocEntry]:
        return list(filter(lambda entry: entry.contains_blog_category(), self.__entries.values()))

    def items_filtered_non_blog_category(self) -> list[DocEntry]:
        return list(filter(lambda entry: not entry.contains_blog_category(), self.__entries.values()))

    def size(self) -> int:
        return len(self.__entries)

    def is_empty(self) -> bool:
        return len(self.__entries) == 0

    def contains(self, target_entry_id: DocEntryId) -> bool:
        for entry in self.items:
            if entry.id == target_entry_id:
                return True
        return False

    def get(self, entry_id: DocEntryId) -> Optional[DocEntry]:
        for entry in self.items:
            if entry.id == entry_id:
                return entry
        return None

    def pickup_entries(self) -> list[DocEntry]:
        pickup_entries: list[DocEntry] = []
        for entry in self.items:
            if entry.pickup:
                pickup_entries.append(entry)
        return pickup_entries

    def merge(self, docs_entries: DocEntries):
        # existed entry is overwritten
        self.__entries |= docs_entries.items

    def find_by_title(self, title) -> Optional[DocEntry]:
        for entry in self.items:
            if entry.title == title:
                return entry
        return None

    def convert_md_lines(self) -> list[str]:
        return [entry.convert_md_line() for entry in self.items]

    @classmethod
    def new_instance(cls, entry_list: list[DocEntry]) -> DocEntries:
        return DocEntries(entry_list)

    def __eq__(self, other) -> bool:
        if not isinstance(other, self.__class__):
            return False
        if not len(self.__entries) == len(other.__entries):
            return False
        for entry in self.items:
            other_entry = other.get(entry.id)
            if other_entry is None:
                return False
            if not entry.__dict__ == other_entry.__dict__:
                return False
        return True
