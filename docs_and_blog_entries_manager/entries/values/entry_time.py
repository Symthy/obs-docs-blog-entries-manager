from datetime import datetime
from typing import Optional

from ltimes import datetime_functions

ENTRY_DATE_TIME_FORMAT = "%Y-%m-%dT%H:%M:%S"


class EntryDateTime:
    def __init__(self, date_time: datetime = None):
        if date_time is None:
            self.__value: str = self.__current_entry_time()
            return
        self.__value = datetime.strftime(date_time, ENTRY_DATE_TIME_FORMAT)

    @staticmethod
    def __current_entry_time() -> str:
        current_time = datetime_functions.current_datetime()
        return current_time.strftime(ENTRY_DATE_TIME_FORMAT)

    def to_str(self) -> str:
        return self.__value

    def to_datetime(self) -> Optional[datetime]:
        if self.__value is None or len(self.__value) == 0:
            return None
        return datetime.strptime(self.__value, ENTRY_DATE_TIME_FORMAT)

    def to_month_day_str(self) -> str:
        return self.to_datetime().strftime('%Y/%m')
