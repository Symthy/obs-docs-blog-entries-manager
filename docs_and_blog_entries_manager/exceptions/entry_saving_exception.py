from entries.domain.interface import IEntry


class EntrySavingException(Exception):
    def __init__(self, entry: IEntry, original_exception: Exception):
        entry_id = entry.id.value
        entry_name = type(entry).__name__
        super().__init__(f'Failed to save the {entry_name}: {entry_id} (detail: {original_exception})')
