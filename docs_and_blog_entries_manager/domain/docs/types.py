from domain.docs.entity.doc_entries import DocEntries
from domain.docs.entity.doc_entry import DocEntry
from domain.docs.value.doc_entry_id import DocEntryId
from domain.entries.interface import IStoredEntriesLoader, IStoredEntriesModifier, IStoredEntriesAccessor

StoredDocEntriesLoader = IStoredEntriesLoader[DocEntries, DocEntry, DocEntryId]
StoredDocEntriesModifier = IStoredEntriesModifier[DocEntries, DocEntry, DocEntryId]
StoredDocEntriesAccessor = IStoredEntriesAccessor[DocEntries, DocEntry, DocEntryId]
