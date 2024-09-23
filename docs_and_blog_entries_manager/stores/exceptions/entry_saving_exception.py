from entries.domain.interface import IEntry


class EntrySavingException(Exception):
    def __init__(self, entry: IEntry, original_exception: Exception):
        super().__init__(f'Failed to save the {entry.entry_type}: {entry} (detail: {original_exception})')
