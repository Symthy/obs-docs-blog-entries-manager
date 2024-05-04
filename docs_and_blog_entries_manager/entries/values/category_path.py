from __future__ import annotations

from typing import List


class CategoryPath:
    def __init__(self, category_path: str):
        if category_path == '':
            raise ValueError(f'Invalid category path: {category_path}')
        self.__values: List[str] = category_path.split('/')

    @property
    def value(self) -> str:
        return '/'.join(self.__values)

    @property
    def length(self) -> int:
        return len(self.__values)

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

    def upper_all_paths(self) -> List[CategoryPath]:
        if len(self.__values) <= 1:
            return []
        paths: List[CategoryPath] = []
        for i in range(len(self.__values) - 1):
            paths.append(CategoryPath('/'.join(self.__values[0:i + 1])))
        return paths

    def __eq__(self, other: CategoryPath) -> bool:
        return self.value == other.value

    def __hash__(self):
        return hash(self.value)

    def __str__(self):
        return self.value
