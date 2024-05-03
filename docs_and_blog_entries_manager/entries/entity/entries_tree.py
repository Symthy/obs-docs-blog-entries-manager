from __future__ import annotations

from typing import List

from entries.interface import IEntries, IConvertibleMarkdownLines


class EntriesTree(IConvertibleMarkdownLines):
    def __init__(self, top_category: str, children: EntriesTree, entries: IEntries):
        self.__top_category = top_category
        self.__children = children
        self.__entries = entries

    @property
    def category(self) -> str:
        return self.__top_category

    def is_exist_category(self, category) -> bool:
        if self.__top_category == category:
            return True
        if self.__children.is_exist_category(category):
            return True
        return False

    def convert_md_lines(self) -> List[str]:
        lines = [f'- {self.__top_category}']
        lines += self.__insert_indent(self.__children.convert_md_lines())
        lines += self.__insert_indent(self.__entries.convert_md_lines())
        return lines

    @staticmethod
    def __insert_indent(md_lines: List[str]) -> List[str]:
        return list(map(lambda line: '  ' + line, md_lines))
