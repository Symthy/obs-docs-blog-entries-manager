from __future__ import annotations

from typing import Generic

from common.result import Result, T, E


class Results(Generic[T, E]):
    def __init__(self, *results: Result[T, E]):
        self.__results = results

    @property
    def success(self) -> bool:
        return len(self.__filtered_error_results()) == 0

    @property
    def failure(self) -> bool:
        return len(self.__filtered_error_results()) > 0

    @property
    def success_values(self) -> list[T]:
        return list(filter(lambda result: result.success, self.__results))

    def merge(self, other: Results) -> Results:
        return Results(*self.__results, *other.__results)

    def print_error(self):
        for result in self.__filtered_error_results():
            result.print_error()

    def print_log(self, success_message: str, key_name: str):
        for result in self.__results:
            result.print_log(success_message, key_name)

    def __filtered_error_results(self) -> list[Result]:
        return list(filter(lambda result: result.failure, self.__results))
