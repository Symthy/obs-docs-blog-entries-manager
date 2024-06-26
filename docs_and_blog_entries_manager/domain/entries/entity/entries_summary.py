from typing import List

from domain.entries.entity.entries_tree_roots import EntriesTreeRoots
from domain.entries.interface import IEntries


class EntriesSummary:
    __PICKUP_ENTRY_HEAD_LINE = 'Pickup:'
    __ALL_ENTRY_HEAD_LINE = 'All:'

    def __init__(self, title: str, entries_tree_roots: EntriesTreeRoots, pickup_entries: IEntries = None):
        self.__title = title
        self.__pickup_entries = pickup_entries
        self.__entries_tree_roots = entries_tree_roots

    @property
    def __pickup_entry_lines(self) -> List[str]:
        return self.__pickup_entries.convert_md_lines()

    @property
    def __entry_tree_lines(self) -> List[str]:
        return self.__entries_tree_roots.convert_md_lines()

    @property
    def title(self):
        return self.__title

    @property
    def all_entry_lines(self) -> List[str]:
        lines: List[str] = []
        if not self.__pickup_entries.is_empty():
            lines.append(self.__PICKUP_ENTRY_HEAD_LINE)
            lines.extend(self.__pickup_entry_lines)
        lines.append('')
        lines.append(self.__ALL_ENTRY_HEAD_LINE)
        lines.extend(self.__entry_tree_lines)
        return lines

    @property
    def list_text(self) -> str:
        return '\n'.join(self.all_entry_lines)

    @property
    def content(self) -> str:
        return f'{self.__title}\n\n{self.list_text}'
