from enum import Enum


class EntryType(Enum):
    BLOG = 1
    DOC = 2

    def __str__(self):
        return f'{self.name.lower()} entry'
