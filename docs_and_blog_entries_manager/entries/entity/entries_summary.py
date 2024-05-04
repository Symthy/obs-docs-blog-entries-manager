from typing import List

from entries.entity.entries_tree_roots import EntriesTreeRoots
from entries.interface import IEntries

PICKUP_ENTRY_HEAD_LINE = 'Pickup:'
ALL_ENTRY_HEAD_LINE = 'All:'


class EntriesSummary:
    def __init__(self, pickup_entries: IEntries, entries_tree_roots: EntriesTreeRoots):
        self.__pickup_entries = pickup_entries
        self.__entries_tree_roots = entries_tree_roots

    @property
    def __pickup_entry_lines(self) -> List[str]:
        return self.__pickup_entries.convert_md_lines()

    @property
    def __all_entry_lines(self) -> List[str]:
        return self.__entries_tree_roots.convert_md_lines()

    @property
    def pickup_and_all_entry_lines(self) -> List[str]:
        lines: List[str] = [PICKUP_ENTRY_HEAD_LINE]
        lines.extend(self.__pickup_entry_lines)
        lines.append('')
        lines.append(ALL_ENTRY_HEAD_LINE)
        lines.extend(self.__all_entry_lines)
        return lines
