from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TypeVar, Generic, Optional

from entries.domain.value.category_path import CategoryPath


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
    def convert_md_lines(self) -> list[str]:
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
    def serialize(self) -> object:
        pass


class IEntries(IConvertibleMarkdownLines, ABC):
    @property
    def items(self) -> list[IEntry]:
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
    def find_by_title(self, title) -> Optional[IEntry]:
        pass

    @abstractmethod
    def new_instance(self, entry_list: list[IEntry]) -> IEntries:
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


class IStoredEntryLoader(ABC, Generic[TS, TI]):
    @abstractmethod
    def load_entry(self, entry_id: TI) -> TS:
        pass


class IStoredEntryModifier(ABC, Generic[TS, TI]):
    @abstractmethod
    def save_entry(self, entry: TS):
        pass


class IStoredEntryAccessor(IStoredEntryLoader[TS, TI], IStoredEntryModifier[TS, TI]):
    @abstractmethod
    def save_entry(self, entry: TS):
        pass

    @abstractmethod
    def load_entry(self, entry_id: TI) -> TS:
        pass


class IStoredEntriesLoader(Generic[TM, TS, TI], IStoredEntryLoader[TS, TI], ABC):
    @abstractmethod
    def load_entries(self) -> TM:
        pass

    @abstractmethod
    def load_entries_by_ids(self, entry_ids: list[TI] = None) -> TM:
        pass

    @abstractmethod
    def load_entries_by_category_path(self, category_path: CategoryPath) -> TM:
        pass

    @abstractmethod
    def load_pickup_entries(self) -> TM:
        pass


class IStoredEntriesModifier(Generic[TM, TS, TI], IStoredEntryModifier[TS, TI], ABC):
    @abstractmethod
    def save_entries(self, entries: TM):
        pass

    @abstractmethod
    def update_pickup(self, entry_id: TI, pickup: bool):
        pass

    @abstractmethod
    def delete_entry(self, entry_id: TI):
        pass


class IStoredEntriesAccessor(IStoredEntriesLoader[TM, TS, TI], IStoredEntriesModifier[TM, TS, TI], ABC):
    pass
