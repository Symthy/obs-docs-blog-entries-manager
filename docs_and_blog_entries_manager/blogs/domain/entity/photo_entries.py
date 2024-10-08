from __future__ import annotations

from typing import Optional

from .photo_entry import PhotoEntry


class PhotoEntries:
    def __init__(self, images: list[PhotoEntry] = None):
        # key: image file name
        self.__filename_to_photo_entry: dict[str, PhotoEntry] = \
            {} if images is None else {image.image_filename: image for image in images}

    @property
    def items(self) -> list[PhotoEntry]:
        return list(self.__filename_to_photo_entry.values())

    @property
    def image_filenames(self) -> list[str]:
        return list(self.__filename_to_photo_entry.keys())

    def is_exist(self, image_filename: str) -> bool:
        return image_filename in self.__filename_to_photo_entry

    def is_empty(self) -> bool:
        return len(self.__filename_to_photo_entry) == 0

    def get_entry(self, image_filename: str) -> Optional[PhotoEntry]:
        if not self.is_exist(image_filename):
            return None
        return self.__filename_to_photo_entry[image_filename]

    def get_entries(self, image_filename: list[str]) -> list[PhotoEntry]:
        photo_entries = []
        for image_filename in image_filename:
            photo_entry_opt = self.get_entry(image_filename)
            if photo_entry_opt is None:
                continue
            photo_entries.append(photo_entry_opt)
        return photo_entries

    def non_exist_entries(self, image_filenames: list[str]) -> PhotoEntries:
        photo_entries: list[PhotoEntry] = []
        for existed_photo_entry in self.__filename_to_photo_entry.values():
            if existed_photo_entry.image_filename not in image_filenames:
                photo_entries.append(existed_photo_entry)
        return PhotoEntries(photo_entries)

    def get_syntax(self, image_filename: str) -> Optional[str]:
        entry = self.get_entry(image_filename)
        return None if entry is None else entry.syntax

    def merge(self, photo_entries: PhotoEntries) -> PhotoEntries:
        # overwrite
        merged_filename_to_photo_entry = self.__filename_to_photo_entry | photo_entries.__filename_to_photo_entry
        return PhotoEntries(list(merged_filename_to_photo_entry.values()))

    def serialize(self) -> dict[str, dict[str, str]]:
        entry_json_list = list(map(lambda e: e.serialize(), self.items))
        dump_json = {}
        for entry_json in entry_json_list:
            dump_json |= entry_json
        return dump_json

    @staticmethod
    def deserialize(filename_to_entry_json: dict[str, dict[str, str]]):
        photo_entry_dict = {}
        for image_filename, photo_entry_json in filename_to_entry_json.items():
            if len(photo_entry_json) > 0:
                photo_entry_dict[image_filename] = PhotoEntry.deserialize(image_filename, photo_entry_json)
        return PhotoEntries(list(photo_entry_dict.values()))
