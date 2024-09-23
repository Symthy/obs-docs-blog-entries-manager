from entries.domain.interface import IEntryDeserializer
from entries.domain.interface import IStoredEntryAccessor, TS, TI
from files import json_file
from files.value import FilePath, DirectoryPath
from stores.exceptions.entry_deleting_exception import EntryDeletingException
from stores.exceptions.entry_loading_exception import EntryLoadingException
from stores.exceptions.entry_saving_exception import EntrySavingException


class StoredEntryAccessor(IStoredEntryAccessor[TS, TI]):
    """
    単一のentryファイルの読み書きを担当
    """

    def __init__(self, stored_entry_dir_path: DirectoryPath, entry_deserializer: IEntryDeserializer):
        self.__stored_entry_dir_path = stored_entry_dir_path
        self.__entry_deserializer = entry_deserializer

    def __build_stored_json_path(self, entry_id: TI) -> FilePath:
        return self.__stored_entry_dir_path.add_file(f'{entry_id.value}.json')

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
        try:
            self.__build_stored_json_path(entry_id).remove_file()
        except Exception as e:
            raise EntryDeletingException(entry_id, e)
