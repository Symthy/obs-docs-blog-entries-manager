from __future__ import annotations

from datetime import datetime

from ltimes import datetime_functions

ENTRY_DATE_TIME_FORMAT = "%Y-%m-%dT%H:%M:%S%z"
DATE_TIME_FORMAT_NUMBER_SEQUENCE = "%Y%m%d%H%M%S"


class EntryDateTime:
    def __init__(self, date_time: datetime = None):
        if date_time is None:
            self.__value: datetime = self.__current_entry_time()
            return
        self.__value: datetime = date_time

    @staticmethod
    def __current_entry_time() -> datetime:
        return datetime_functions.current_datetime()

    def to_str(self) -> str:
        return datetime.strftime(self.__value, ENTRY_DATE_TIME_FORMAT)

    def to_str_with_num_sequence(self) -> str:
        return datetime.strftime(self.__value, DATE_TIME_FORMAT_NUMBER_SEQUENCE)

    def to_datetime(self) -> datetime:
        return self.__value

    def to_month_day_str(self) -> str:
        return self.to_datetime().strftime('%Y/%m')

    def is_time_after(self, other: EntryDateTime) -> bool:
        return self.__value > other.__value
