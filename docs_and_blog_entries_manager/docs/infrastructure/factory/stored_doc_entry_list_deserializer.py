from common.constants import DOC_ENTRY_LIST_PATH
from docs.domain.value import DocEntryId
from docs.infrastructure.types import StoredDocEntryListHolder
from files.value import FilePath
from stores.factory.stored_entry_list_deserializer import IStoredEntryListDeserializer, StoredEntryListDeserializer


class StoredDocEntryListDeserializer(IStoredEntryListDeserializer):
    def __init__(self, entry_list_file_path: FilePath = DOC_ENTRY_LIST_PATH):
        self.__delegator = StoredEntryListDeserializer(DocEntryId.new_instance, entry_list_file_path)

    def deserialize(self) -> StoredDocEntryListHolder:
        return self.__delegator.deserialize()
