from __future__ import annotations

from abc import ABC, abstractmethod
from typing import List, Dict


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
    def id(self) -> IEntryId:
        # required override
        raise Exception('Unimplemented!! (IEntry.id)')

    @property
    def title(self) -> str:
        # required override
        raise Exception('Unimplemented!! (IEntry.title)')

    @property
    def category_path(self) -> str:
        # required override
        raise Exception('Unimplemented!! (IEntry.top_category)')

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
        raise Exception('Unimplemented!! (IEntries.entry_list)')

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


class IEntryId(ABC):
    @property
    def value(self) -> str:
        # required override
        raise Exception('Unimplemented!! (IEntryId.value)')

    @abstractmethod
    def new_instance(self, entry_id: str) -> IEntryId:
        pass
