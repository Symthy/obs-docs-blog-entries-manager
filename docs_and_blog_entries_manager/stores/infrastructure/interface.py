from abc import ABC, abstractmethod
from typing import Generic

from entries.domain.interface import TI, TM, TS


class IReadableStoredEntryList(ABC, Generic[TM, TS, TI]):

    @property
    def entry_ids(self) -> list[TI]:
        # required override
        raise Exception('Unimplemented!! (IReadableStoredEntryList.entry_ids)')

    @property
    def pickup_entry_ids(self) -> list[TI]:
        # required override
        raise Exception('Unimplemented!! (IReadableStoredEntryList.pickup_entry_ids)')

    @property
    def update_at(self) -> str:
        # required override
        raise Exception('Unimplemented!! (IReadableStoredEntryList.update_at)')

    @abstractmethod
    def exist_id(self, entry_id: TI) -> bool:
        pass

    @abstractmethod
    def is_pickup(self, entry_id: TI) -> bool:
        pass


class IWritableStoredEntryList(ABC, Generic[TM, TS, TI]):
    @abstractmethod
    def push_entry(self, entry: TS):
        pass

    @abstractmethod
    def push_entries(self, entries: TM):
        pass

    @abstractmethod
    def update_pickup(self, entry_id: TI, pickup: bool):
        pass

    @abstractmethod
    def delete_entry(self, entry_id: TI):
        pass


class ISerializableStoredEntryList(ABC):
    @abstractmethod
    def serialize(self) -> dict[str, dict[str, bool]]:
        pass


class IStoredEntryListHolder(IReadableStoredEntryList[TM, TS, TI], IWritableStoredEntryList[TM, TS, TI],
                             ISerializableStoredEntryList, ABC):
    pass
