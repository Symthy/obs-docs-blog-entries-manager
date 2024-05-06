from domain.entries.interface import IEntryId


class EntryLoadingException(Exception):
    def __init__(self, entry_id: IEntryId, original_exception: Exception):
        entry_id = entry_id.value
        entry_name = type(entry_id).__name__[:2]  # 末尾の Id を除去
        super().__init__(f'Failed to load the {entry_name}: {entry_id} (detail: {original_exception})')
