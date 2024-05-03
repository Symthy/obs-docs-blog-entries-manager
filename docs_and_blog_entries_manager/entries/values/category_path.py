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
    def top(self) -> str:
        return self.__values[0]

    @property
    def end(self) -> str:
        return self.__values[-1]

    def join(self, category_name: str) -> CategoryPath:
        return CategoryPath(self.value + '/' + category_name)

    def starts_with(self, other: CategoryPath) -> bool:
        """
        前方一致
        """
        for i in range(len(other.__values)):
            if self.__values[i] != other.__values[i]:
                return False
        return True

    def equals(self, other: CategoryPath) -> bool:
        return self.value == other.value
