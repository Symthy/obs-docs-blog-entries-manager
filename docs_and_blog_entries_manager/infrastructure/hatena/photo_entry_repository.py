from typing import Optional, List

from docs_and_blog_entries_manager.api.api_client import ApiClient
from domain.blogs.entity.photo.photo_entries import PhotoEntries
from domain.blogs.entity.photo.photo_entry import PhotoEntry
from domain.blogs.value.photo_entry_id import PhotoEntryId
from files import image_file, file_path
from infrastructure.hatena.api.photo_response_parser import PhotoEntryResponseBody
from infrastructure.hatena.templates import request_formats
from logs.logger import Logger


class PhotoEntryRepository:
    def __init__(self, api_client: ApiClient):
        self.__api_client = api_client

    # GET Photo
    def find_id(self, entry_id: PhotoEntryId) -> Optional[PhotoEntry]:
        path = f'edit/{entry_id.value}'
        Logger.info(f'GET Photo: {entry_id.value}')
        xml_string_opt = self.__api_client.get(path)
        return PhotoEntryResponseBody(xml_string_opt).parse('')

    # POST photo
    def post_all(self, image_file_paths: List[str]) -> PhotoEntries:
        photo_entries: List[PhotoEntry] = []
        for image_path in image_file_paths:
            entry_opt = self.post(image_path)
            if entry_opt is not None:
                photo_entries.append(entry_opt)
        return PhotoEntries(photo_entries)

    def post(self, image_file_path: str) -> Optional[PhotoEntry]:
        def __build_hatena_photo_entry_body() -> Optional[str]:
            # Todo: refactor use library
            __PIC_EXTENSION_TO_CONTENT_TYPE = {
                'jpg': 'image/jpeg',
                'jpeg': 'image/jpeg',
                'png': 'image/png',
                'gif': 'image/gif',
                'bmp': 'image/bmp',
                'svg': 'image/svg+xml',
            }
            split_str = image_file_path.rsplit('.', 1)
            path_without_extension = split_str[0]
            file_name_without_extension = file_path.get_file_name(path_without_extension)
            title = file_name_without_extension
            extension = split_str[-1].lower()
            if not extension in __PIC_EXTENSION_TO_CONTENT_TYPE:
                Logger.warn(f'Non support image file extension: {image_file_path}')
                return None
            b64_pic_data = image_file.read_b64(image_file_path)
            return request_formats.build_photo_entry_post_xml_body(title,
                                                                   __PIC_EXTENSION_TO_CONTENT_TYPE[extension],
                                                                   b64_pic_data)

        body = __build_hatena_photo_entry_body()
        Logger.info(f'POST Photo: {image_file_path}')
        xml_string_opt = self.__api_client.post(body, 'post')
        image_filename = file_path.get_file_name(image_file_path)
        return PhotoEntryResponseBody(xml_string_opt).parse(image_filename)

    # UPDATE(DELETE+POST) photo
    # because PUT can change title only
    def put(self, image_file_path: str, photo_entry: PhotoEntry) -> Optional[PhotoEntry]:
        # Todo: error
        self.__delete(photo_entry)
        return self.post(image_file_path)

    # DELETE
    def delete_all(self, photo_entries: PhotoEntries):
        for photo_entry in photo_entries.items:
            self.__delete(photo_entry)

    def __delete(self, photo_entry: PhotoEntry):
        path = f'edit/{photo_entry.id}'
        res = self.__api_client.delete(path)
        if res is None:
            # Todo: error
            return None
        Logger.info(f'DELETE Photo: {photo_entry.id}')
