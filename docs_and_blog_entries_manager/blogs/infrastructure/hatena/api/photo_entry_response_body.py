from typing import Optional

from blogs.domain.entity import PhotoEntry
from blogs.infrastructure.hatena.api.xml import PhotoEntryXmlParser


# def print_xml_children(root: ET.Element):
#     """
#     for debug
#     """
#     for child in root:
#         print(child.tag)

# Todo: refactor
class PhotoEntryResponseBody:

    def __init__(self, response_xml: Optional[str]):
        self.__response_xml = response_xml
        self.__photo_entry_xml_parser = PhotoEntryXmlParser()

    def parse(self, image_filename: str) -> Optional[PhotoEntry]:
        if self.__response_xml is None:
            return None
        return self.__photo_entry_xml_parser.parse(self.__response_xml, image_filename)
