from abc import ABC

from docs.domain.value import DocEntryId
from stores.infrastructure.interface import IReadableStoredEntryList


class ReadableDocEntryListHolder(IReadableStoredEntryList[DocEntryId], ABC):
    pass
