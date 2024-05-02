from typing import Optional

from blogs.datasources.hatena.api.photo_response_parser import PhotoEntryResponseBody
from blogs.datasources.hatena.templates import request_formats
from docs_and_blog_entries_manager.api.api_client import ApiClient
from docs_and_blog_entries_manager.blogs.entity.photo.photo_entry import PhotoEntry
from docs_and_blog_entries_manager.ltimes import datetime_functions
from files import image_file, file_path
from logs.logger import Logger


class PhotoEntryRepository:
    def __init__(self, api_client: ApiClient):
        self.__api_client = api_client

    # GET Photo
    def find_id(self, entry_id: str) -> Optional[PhotoEntry]:
        path = f'edit/{entry_id}'
        Logger.info(f'GET Photo: {entry_id}')
        xml_string_opt = self.__api_client.get(path)
        return PhotoEntryResponseBody(xml_string_opt).parse('')

    # POST photo
    # Todo: 引数をPhotoEntryにできないか
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
            title = f'{datetime_functions.resolve_current_time_sequence()}_{file_name_without_extension}'
            extension = split_str[1].lower()
            if not extension in __PIC_EXTENSION_TO_CONTENT_TYPE:
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
    # Todo: 引数をPhotoEntryのみにできないか
    def put(self, image_file_path: str, photo_entry: PhotoEntry) -> Optional[PhotoEntry]:
        path = f'edit/{photo_entry.id}'
        Logger.info('DELETE Photo')
        self.__api_client.delete(path)
        return self.post(image_file_path)
