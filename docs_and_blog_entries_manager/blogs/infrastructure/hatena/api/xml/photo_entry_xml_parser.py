from blogs.domain.entity import PhotoEntry
from blogs.domain.value import PhotoEntryId
from blogs.infrastructure.hatena.api.xml import entry_xml
from ltimes import datetime_functions


class PhotoEntryXmlParser:
    __PHOTO_ENTRY_XML_NAMESPACE = '{http://purl.org/atom/ns#}'
    __PHOTO_ENTRY_HATENA_XML_NAMESPACE = '{http://www.hatena.ne.jp/info/xmlns#}'

    def parse(self, response_xml: str, image_filename: str):
        root_node = entry_xml.convert_root_node(response_xml)
        # print_xml_children(root)
        hatena_entry_id = root_node.find(self.__PHOTO_ENTRY_XML_NAMESPACE + 'id').text
        if hatena_entry_id is None:
            return None
        photo_entry_id = PhotoEntryId(hatena_entry_id.rsplit('-', 1)[1])
        syntax = root_node.find(self.__PHOTO_ENTRY_HATENA_XML_NAMESPACE + 'syntax').text
        image_url = root_node.find(self.__PHOTO_ENTRY_HATENA_XML_NAMESPACE + 'imageurl').text
        # don't know if the API response includes the update time.
        updated_datetime = datetime_functions.current_datetime()
        return PhotoEntry(image_filename, photo_entry_id, syntax, image_url, updated_datetime)
