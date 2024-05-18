from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Dict
from typing import List, TypeVar, Generic

from domain.entries.values.category_path import CategoryPath


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

    @property
    def pickup(self) -> bool:
        # required override
        raise Exception('Unimplemented!! (IEntry.pickup)')

    @abstractmethod
    def update_pickup(self, pickup: bool) -> IEntry:
        pass

    @abstractmethod
    def convert_id_to_title(self) -> Dict[str, str]:
        pass

    @abstractmethod
    def serialize(self) -> object:
        pass

    @abstractmethod
    def deserialize(self, json_data: Dict[str, any]):
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

    @classmethod
    @abstractmethod
    def new_instance(cls, entry_id: str) -> IEntryId:
        pass


class IEntryDeserializer(ABC):
    @abstractmethod
    def deserialize(self, json_data: dict[str, any]) -> IEntry:
        pass


TM = TypeVar('TM', bound=IEntries)
TS = TypeVar('TS', bound=IEntry)
TI = TypeVar('TI', bound=IEntryId)


class IStoredEntryAccessor(ABC, Generic[TS, TI]):
    def load_entry(self, entry_id: TI) -> TS:
        pass

    def save_entry(self, entry: TS):
        pass


class IStoredEntriesAccessor(ABC, Generic[TM, TS, TI]):
    def load_entries(self) -> TM:
        pass

    def load_entries_by_id(self, entry_ids: List[TI] = None) -> TM:
        pass

    def load_entries_by_category_path(self, category_path: CategoryPath) -> TM:
        pass

    def load_pickup_entries(self) -> TM:
        pass

    def save_entries(self, entries: TM):
        pass

    def search_entry_ids(self, keyword: str) -> List[TI]:
        pass

    def has_entry(self, entry_id: TI) -> bool:
        pass
