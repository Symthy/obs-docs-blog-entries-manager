from domain.entries.interface import IEntryDeserializer
from domain.entries.interface import IStoredEntryAccessor, TS, TI
from exceptions.entry_loading_exception import EntryLoadingException
from exceptions.entry_saving_exception import EntrySavingException
from files import json_file, file_system


class _StoredEntryAccessor(IStoredEntryAccessor[TS, TI]):

    def __init__(self, stored_entry_dir_path: str, entry_deserializer: IEntryDeserializer):
        self.__stored_entry_dir_path = stored_entry_dir_path
        self.__entry_deserializer = entry_deserializer

    def __build_stored_json_path(self, entry_id: TI):
        return file_system.join_path(self.__stored_entry_dir_path, f'{entry_id.value}.json')

    def load_entry(self, entry_id: TI) -> TS:
        try:
            stored_file_path = self.__build_stored_json_path(entry_id)
            json_data: dict = json_file.load(stored_file_path)
            return self.__entry_deserializer.deserialize(json_data)
        except Exception as e:
            raise EntryLoadingException(entry_id, e)

    def save_entry(self, entry: TS):
        try:
            stored_json_path = self.__build_stored_json_path(entry.id)
            json_file.save(stored_json_path, entry)
        except Exception as e:
            raise EntrySavingException(entry, e)

    def update_pickup(self, entry_id: TI, pickup: bool):
        entry = self.load_entry(entry_id)
        updated_entry = entry.update_pickup(pickup)
        self.save_entry(updated_entry)

    def delete_entry(self, entry_id: TI):
        file_system.remove_file(self.__build_stored_json_path(entry_id))
