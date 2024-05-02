from __future__ import annotations

from typing import Optional, List

from docs_and_blog_entries_manager.blogs.entity.photo.photo_entry import PhotoEntry


class PhotoEntries:
    def __init__(self, images_dict: Optional[dict[str, PhotoEntry]] = None):
        # key: image file name
        self.__filename_to_photo_entry: dict[str, PhotoEntry] = {} if images_dict is None else images_dict

    @property
    def items(self) -> List[PhotoEntry]:
        return list(self.__filename_to_photo_entry.values())

    @property
    def image_filenames(self) -> List[str]:
        return list(self.__filename_to_photo_entry.keys())

    def is_exist(self, image_filename: str) -> bool:
        return image_filename in self.__filename_to_photo_entry

    def is_empty(self) -> bool:
        return len(self.__filename_to_photo_entry) == 0

    def get_entry(self, image_filename: str) -> Optional[PhotoEntry]:
        if not self.is_exist(image_filename):
            return None
        return self.__filename_to_photo_entry[image_filename]

    def get_syntax(self, image_filename: str) -> Optional[str]:
        entry = self.get_entry(image_filename)
        return None if entry is None else entry.syntax

    def merge(self, photo_entries: PhotoEntries):
        # overwrite
        self.__filename_to_photo_entry |= photo_entries.__filename_to_photo_entry

    def serialize(self) -> dict[str, dict[str, str]]:
        entry_json_list = list(map(lambda e: e.serialize(), self.items))
        dump_json = {}
        for entry_json in entry_json_list:
            dump_json |= entry_json
        return dump_json

    @classmethod
    def deserialize(cls, filename_to_entry_json: dict[str, dict[str, str]]):
        photo_entry_dict = {}
        for image_filename, photo_entry_json in filename_to_entry_json.items():
            if len(photo_entry_json) > 0:
                photo_entry_dict[image_filename] = PhotoEntry.deserialize(image_filename, photo_entry_json)
        return PhotoEntries(photo_entry_dict)
