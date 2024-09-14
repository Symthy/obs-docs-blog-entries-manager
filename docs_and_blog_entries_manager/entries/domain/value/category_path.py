from __future__ import annotations

from common.constants import NON_CATEGORY_NAME
from files.value import DirectoryPath


class CategoryPath:
    def __init__(self, category_path: str):
        if category_path == '':
            raise ValueError(f'Invalid category path: {category_path}')
        self.__values: list[str] = category_path.split('/')

    @staticmethod
    def non_category() -> CategoryPath:
        return CategoryPath(NON_CATEGORY_NAME)

    @property
    def value(self) -> DirectoryPath:
        return DirectoryPath(*self.__values)

    @property
    def length(self) -> int:
        return len(self.__values)

    @property
    def is_empty(self) -> bool:
        return self.length == 0

    @property
    def top(self) -> str:
        return self.__values[0]

    @property
    def end(self) -> str:
        return self.__values[-1]

    def join(self, category_name: str) -> CategoryPath:
        return CategoryPath(self.value + '/' + category_name)

    def purge_end(self) -> CategoryPath:
        return CategoryPath('/'.join(self.__values[:-1]))

    def starts_with(self, other: CategoryPath) -> bool:
        """
        前方完全一致
        """
        length = self.length if self.length < other.length else other.length
        for i in range(length):
            if self.__values[i] != other.__values[i]:
                return False
        return True

    def is_child(self, other: CategoryPath) -> bool:
        if self.length + 1 != other.length:
            return False
        return self.starts_with(other)

    def exist_parent(self):
        return len(self.__values) > 1

    def upper_all_paths(self) -> list[CategoryPath]:
        if len(self.__values) <= 1:
            return []
        paths: list[CategoryPath] = []
        for i in range(len(self.__values) - 1):
            paths.append(CategoryPath('/'.join(self.__values[0:i + 1])))
        return paths

    def __to_str(self) -> str:
        return '/'.join(self.__values)

    def __eq__(self, other: CategoryPath) -> bool:
        return self.__to_str() == other.__to_str()

    def __hash__(self):
        return hash(self.__to_str())

    def __str__(self):
        return self.__to_str()
