from __future__ import annotations

from typing import List, Optional

from domain.entries.interface import IEntries, IConvertibleMarkdownLines
from domain.entries.values.category_path import CategoryPath


class EntriesTree(IConvertibleMarkdownLines):
    def __init__(self, category_path: CategoryPath, entries: IEntries, children: List[EntriesTree] = None):
        self.__category_path: CategoryPath = category_path
        self.__children: List[EntriesTree] = children if children is not None else []
        self.__entries: IEntries = entries

    @property
    def category_path(self) -> CategoryPath:
        return self.__category_path

    @property
    def children(self) -> List[EntriesTree]:
        return self.__children

    @property
    def child_category_paths(self) -> List[CategoryPath]:
        return list(map(lambda c: c.category_path, self.__children))

    @property
    def entries(self) -> IEntries:
        return self.__entries

    def equals_category_path(self, category_path: CategoryPath) -> bool:
        return self.__category_path == category_path

    def search_node(self, category_path: CategoryPath) -> Optional[EntriesTree]:
        if self.__category_path == category_path:
            return self
        for child_tree in self.__children:
            if child_tree.equals_category_path(category_path):
                return child_tree
            if category_path.starts_with(child_tree.category_path):
                return child_tree.search_node(category_path)
        return None

    def convert_md_lines(self) -> List[str]:
        lines = [f'- {self.__category_path.end}']
        for child in self.__children:
            lines += self.__insert_indent(child.convert_md_lines())
        lines += self.__insert_indent(self.__entries.convert_md_lines())
        return lines

    @staticmethod
    def __insert_indent(md_lines: List[str]) -> List[str]:
        return list(map(lambda line: '  ' + line, md_lines))
