from entries.domain.interface import IEntryId


class EntryDeletingException(Exception):
    def __init__(self, entry_id: IEntryId, original_exception: Exception):
        super().__init__(f'Failed to delete the {entry_id.entry_type}: {entry_id} (detail: {original_exception})')
