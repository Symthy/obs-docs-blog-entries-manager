from files import json_file, file_system
from store.interface import TS, IStoredEntryAccessor


class StoredEntryAccessor(IStoredEntryAccessor[TS]):

    def __init__(self, dump_dir_path):
        self.__stored_entry_dir_path = dump_dir_path

    def __build_stored_json_path(self, entry_id: str):
        return file_system.join_path(self.__stored_entry_dir_path, f'{entry_id}.json')

    def load_entry(self, entry_id: str) -> TS:
        stored_file_path = self.__build_stored_json_path(entry_id)
        json_data: dict = json_file.load(stored_file_path)
        return TS.deserialize(json_data)

    def save_entry(self, entry: TS):
        stored_json_path = self.__build_stored_json_path(entry.id)
        entry_json = json_file.load(stored_json_path) if file_system.exist_file(stored_json_path) else None
        dump_data = entry.serialize(entry_json)
        json_file.save(stored_json_path, dump_data)
