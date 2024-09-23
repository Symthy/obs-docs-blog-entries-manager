from entries.domain.interface import IEntryId


class EntryLoadingException(Exception):
    def __init__(self, entry_id: IEntryId, original_exception: Exception):
        super().__init__(f'Failed to load the {entry_id.entry_type}: {entry_id} (detail: {original_exception})')
