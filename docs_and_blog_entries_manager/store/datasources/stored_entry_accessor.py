from files import json_file, file_system
from store.interface import TS, IStoredEntryAccessor, TI


class StoredEntryAccessor(IStoredEntryAccessor[TS, TI]):

    def __init__(self, stored_entry_dir_path: str):
        self.__stored_entry_dir_path = stored_entry_dir_path

    def __build_stored_json_path(self, entry_id: TI):
        return file_system.join_path(self.__stored_entry_dir_path, f'{entry_id.value}.json')

    def load_entry(self, entry_id: TI) -> TS:
        stored_file_path = self.__build_stored_json_path(entry_id)
        json_data: dict = json_file.load(stored_file_path)
        return TS.deserialize(json_data)

    def save_entry(self, entry: TS):
        stored_json_path = self.__build_stored_json_path(entry.id)
        json_file.save(stored_json_path, entry)
