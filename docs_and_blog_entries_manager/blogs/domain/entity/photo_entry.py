from __future__ import annotations

from datetime import datetime
from typing import Optional

from blogs.domain.value import PhotoEntryId
from docs_and_blog_entries_manager.ltimes import datetime_functions


class PhotoEntry:
    FIELD_ID = 'id'
    FIELD_SYNTAX = 'syntax'
    FIELD_IMAGE_URL = 'image_url'
    FIELD_UPDATED_AT = 'updated_at'

    def __init__(self, image_filename: str, entry_id: PhotoEntryId, syntax: str, image_url: str,
                 updated_at: Optional[datetime] = None):
        self.__image_filename = image_filename
        self.__id = entry_id
        self.__syntax = syntax
        self.__image_url = image_url
        self.__updated_at = updated_at

    @property
    def image_filename(self) -> str:
        return self.__image_filename

    @property
    def id(self) -> PhotoEntryId:
        return self.__id

    @property
    def syntax(self) -> str:
        return self.__syntax

    @property
    def image_url(self):
        return self.__image_url

    @property
    def updated_at(self) -> str:
        return datetime_functions.convert_to_entry_time_str(self.__updated_at)

    def is_after_updated_time(self, specified_time: datetime) -> bool:
        return specified_time > self.__updated_at

    def serialize(self) -> dict[str, dict[str, str]]:
        return {
            self.__image_filename: {
                PhotoEntry.FIELD_ID: self.__id.value,
                PhotoEntry.FIELD_SYNTAX: self.__syntax,
                PhotoEntry.FIELD_IMAGE_URL: self.__image_url,
                PhotoEntry.FIELD_UPDATED_AT: self.updated_at
            }
        }

    @classmethod
    def deserialize(cls, image_filename: str, dump_data: dict[str, str]):
        return PhotoEntry(
            image_filename,
            PhotoEntryId(dump_data[PhotoEntry.FIELD_ID]),
            dump_data[PhotoEntry.FIELD_SYNTAX],
            dump_data[PhotoEntry.FIELD_IMAGE_URL],
            datetime_functions.convert_entry_time_str_to_datetime(dump_data[PhotoEntry.FIELD_UPDATED_AT])
        )
