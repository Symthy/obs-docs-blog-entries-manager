from abc import ABC, abstractmethod
from typing import Generic

from entries.domain.interface import TI


class IReadableStoredEntryList(ABC, Generic[TI]):

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
