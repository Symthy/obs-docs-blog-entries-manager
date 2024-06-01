from abc import ABC, abstractmethod
from typing import TypeVar, Generic, Union, Optional

from logs.logger import Logger

T = TypeVar('T')
E = TypeVar('E')


class IResultLogger(ABC):

    @abstractmethod
    def print_log(self, message: str, key_name: Optional[str]):
        pass

    @abstractmethod
    def print_error(self):
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

    @property
    def value(self):
        return self.__value

    def print_log(self, success_message: str, key_name: Optional[str]):
        if self.success:
            Logger.info(f'{success_message} ({key_name}={self.__value})')
        if self.failure:
            Logger.error(self.__error)

    def print_error(self):
        Logger.error(self.__error)
