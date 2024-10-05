from docs.domain.entity import DocEntries, DocEntry
from docs.domain.value import DocEntryId
from stores.infrastructure.interface import IReadableStoredEntryList, IStoredEntryListHolder

ReadableDocEntryListHolder = IReadableStoredEntryList[DocEntries, DocEntry, DocEntryId]

StoredDocEntryListHolder = IStoredEntryListHolder[DocEntries, DocEntry, DocEntryId]
