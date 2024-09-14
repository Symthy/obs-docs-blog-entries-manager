from __future__ import annotations

from typing import Optional

from blogs.domain.value import BlogEntryId
from entries.domain.interface import IEntries
from .blog_entry import BlogEntry


class BlogEntries(IEntries):
    def __init__(self, entries: list[BlogEntry] = None):
        self.__entries: dict[BlogEntryId, BlogEntry] = {}
        if entries is not None:
            self.__entries = {entry.id: entry for entry in entries}

    @property
    def items(self) -> list[BlogEntry]:
        return list(self.__entries.values())

    def is_empty(self) -> bool:
        return len(self.items) == 0

    def contains(self, target_entry_id: BlogEntryId) -> bool:
        for entry in self.items:
            if entry.id == target_entry_id:
                return True
        return False

    def add_entry(self, blog_entry: BlogEntry):
        self.__entries[blog_entry.id] = blog_entry

    def find_by_title(self, title) -> Optional[BlogEntry]:
        for entry in self.items:
            if entry.title == title:
                return entry
        return None

    def merge(self, blog_entries: BlogEntries):
        if blog_entries.is_empty():
            return
        # existed entry is overwritten
        self.__entries |= blog_entries.__entries

    def convert_md_lines(self) -> list[str]:
        return [entry.convert_md_line() for entry in self.items]

    @classmethod
    def new_instance(cls, entry_list: list[BlogEntry]) -> BlogEntries:
        return BlogEntries(entry_list)
