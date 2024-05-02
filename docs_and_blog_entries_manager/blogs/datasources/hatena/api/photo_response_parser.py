from typing import Optional

from blogs.datasources.hatena.api.xml import entry_xml
from blogs.entity.photo.photo_entry import PhotoEntry
from ltimes import datetime_functions


# def print_xml_children(root: ET.Element):
#     """
#     for debug
#     """
#     for child in root:
#         print(child.tag)

# Todo: refactor
class PhotoEntryResponseBody:
    __PHOTO_ENTRY_XML_NAMESPACE = '{http://purl.org/atom/ns#}'
    __PHOTO_ENTRY_HATENA_XML_NAMESPACE = '{http://www.hatena.ne.jp/info/xmlns#}'

    def __init__(self, response_xml: Optional[str]):
        self.__response_xml = response_xml

    def parse(self, image_filename: str) -> Optional[PhotoEntry]:
        if self.__response_xml is None:
            return None
        root_node = entry_xml.convert_root_node(self.__response_xml)
        # print_xml_children(root)
        hatena_entry_id = root_node.find(self.__PHOTO_ENTRY_XML_NAMESPACE + 'id').text
        if hatena_entry_id is None:
            return None
        photo_entry_id = hatena_entry_id.rsplit('-', 1)[1]
        syntax = root_node.find(self.__PHOTO_ENTRY_HATENA_XML_NAMESPACE + 'syntax').text
        image_url = root_node.find(self.__PHOTO_ENTRY_HATENA_XML_NAMESPACE + 'imageurl').text
        # don't know if the API response includes the update time.
        updated_datetime = datetime_functions.get_current_datetime()
        return PhotoEntry(image_filename, photo_entry_id, syntax, image_url, updated_datetime)
