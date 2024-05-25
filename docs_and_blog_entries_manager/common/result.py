from abc import ABC
from typing import TypeVar, Generic, Union

from logs.logger import Logger

T = TypeVar('T')
E = TypeVar('E')


class IResultLogger(ABC):
    def print_log(self):
        pass


class Result(Generic[T, E]):
    def __init__(self, value: Union[T, None] = None, error: Union[E, None] = None):
        self.__value = value
        self.__error = error

    @property
    def success(self) -> bool:
        return self.__error is None

    @property
    def failure(self) -> bool:
        return self.__error is not None

    def print_log(self):
        if self.success:
            Logger.info(self.__value)
        if self.failure:
            Logger.error(self.__error)
