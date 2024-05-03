from __future__ import annotations

from abc import ABC, abstractmethod
from typing import List, Dict

from docs_and_blog_entries_manager.logs.logger import Logger


class ISerializableObject(ABC):
    @abstractmethod
    def serialize(self) -> object:
        pass


class IConvertibleMarkdownLine(ABC):
    @abstractmethod
    def convert_md_line(self) -> str:
        pass


class IConvertibleMarkdownLines(ABC):
    @abstractmethod
    def convert_md_lines(self) -> List[str]:
        pass


class IEntry(ISerializableObject, IConvertibleMarkdownLine, ABC):
    @property
    def id(self) -> str:
        # required override
        Logger.error('Unimplemented!! (IEntry.id)')
        return ''

    @property
    def title(self) -> str:
        # required override
        Logger.error('Unimplemented!! (IEntry.title)')
        return ''

    @property
    def category_path(self) -> str:
        # required override
        Logger.error('Unimplemented!! (IEntry.top_category)')
        return ''

    @abstractmethod
    def convert_id_to_title(self) -> Dict[str, str]:
        pass

    @abstractmethod
    def deserialize(self, json_data: dict[str, any]):
        pass


class IEntries(IConvertibleMarkdownLines, ABC):
    @property
    def items(self) -> List[IEntry]:
        # required override
        Logger.error('Unimplemented!! (IEntries.entry_list)')
        return []

    @abstractmethod
    def is_empty(self) -> bool:
        pass

    @abstractmethod
    def contains(self, target_entry_id: str) -> bool:
        pass

    @abstractmethod
    def merge(self, entries: IEntries):
        pass

    @abstractmethod
    def new_instance(self, entry_list: List[IEntry]) -> IEntries:
        pass
