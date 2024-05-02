from __future__ import annotations

from typing import List

from docs_and_blog_entries_manager.blogs.entity.blog_entry import BlogEntry
from docs_and_blog_entries_manager.entries.interface import IEntries


class BlogEntries(IEntries):
    def __init__(self, entries: List[BlogEntry] = None):
        # Todo: examination. use dict? see
        self.__entries: dict[str, BlogEntry] = {}
        if entries is not None:
            self.__entries = {entry.id: entry for entry in entries}

    @property
    def items(self) -> List[BlogEntry]:
        return list(self.__entries.values())

    def is_empty(self) -> bool:
        return len(self.items) == 0

    def contains(self, target_entry_id: str) -> bool:
        for entry in self.items:
            if entry.id == target_entry_id:
                return True
        return False

    def add_entry(self, blog_entry: BlogEntry):
        self.__entries[blog_entry.id] = blog_entry

    def merge(self, blog_entries: BlogEntries):
        if blog_entries.is_empty():
            return
        # existed entry is overwritten
        self.__entries |= blog_entries.__entries

    def convert_md_lines(self) -> List[str]:
        return [entry.convert_md_line() for entry in self.items]

    @classmethod
    def new_instance(cls, entry_list: List[BlogEntry]) -> BlogEntries:
        return BlogEntries(entry_list)
