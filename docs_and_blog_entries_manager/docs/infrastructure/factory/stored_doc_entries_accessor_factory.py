from common.constants import LOCAL_STORE_DIR_PATH
from docs.domain.datasource.interface import StoredDocEntriesAccessor
from docs.domain.entity import DocEntries
from docs.domain.factory import DocEntryDeserializer
from docs.infrastructure.factory.stored_doc_entry_list_deserializer import StoredDocEntryListDeserializer
from docs.infrastructure.types import StoredDocEntryListHolder
from files.value import DirectoryPath
from stores.infrastructure import StoredEntryAccessor, StoredEntriesAccessor


class StoredDocEntriesAccessorFactory:
    def __init__(self, store_dir_path: DirectoryPath = LOCAL_STORE_DIR_PATH):
        self.__store_dir_path = store_dir_path

    def build(self, stored_doc_entry_list: StoredDocEntryListHolder = None) -> StoredDocEntriesAccessor:
        entry_list_file_path = self.__store_dir_path.add_file('doc_entry_list.json')
        stored_doc_entry_dir_path = self.__store_dir_path.add_dir('doc')
        stored_doc_entry_accessor = StoredEntryAccessor(stored_doc_entry_dir_path, DocEntryDeserializer())
        if stored_doc_entry_list is None:
            deserializer = StoredDocEntryListDeserializer(entry_list_file_path)
            return StoredEntriesAccessor(entry_list_file_path, stored_doc_entry_accessor,
                                         deserializer.deserialize(), DocEntries.new_instance)
        return StoredEntriesAccessor(entry_list_file_path, stored_doc_entry_accessor,
                                     stored_doc_entry_list, DocEntries.new_instance)
