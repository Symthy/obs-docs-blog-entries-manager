from typing import Optional, List

from docs_and_blog_entries_manager.common.constants import EXCLUDE_ENTRY_IDS_TXT_PATH
from docs_and_blog_entries_manager.files import config
from domain.blogs.datasource.model.posted_blog_entry import PostedBlogEntry
from domain.blogs.value.blog_entry_id import BlogEntryId
from infrastructure.hatena.api.xml import entry_xml
from infrastructure.hatena.api.xml.blog_entry_xml_parser import BlogEntryXmlParser


# def __print_xml_children(root: ET.Element):
#     """
#     for debug
#     """
#     for child in root:
#         print(child.tag)

# Todo: refactor (xmlはクラス化して隔離した方が良い)
class BlogEntriesResponseBody:
    def __init__(self, response_xml: str, hatena_id: str, summary_entry_id: BlogEntryId):
        self.__hatena_id = hatena_id
        self.__response_xml = response_xml
        self.__exclude_entry_ids = config.read_lines(EXCLUDE_ENTRY_IDS_TXT_PATH)
        self.__exclude_entry_ids.append(summary_entry_id.value)  # exclude summary entry index page]
        self.__blog_entry_xmf_parser = BlogEntryXmlParser(hatena_id)

    def next_page_url(self) -> Optional[str]:
        url = None
        root_node = entry_xml.convert_root_node(self.__response_xml)
        for link in root_node.iter(entry_xml.extract_tag_head(root_node) + 'link'):
            if link.attrib['rel'] == 'next':
                url = link.attrib['href']
                break
        return url

    def parse(self) -> List[PostedBlogEntry]:
        root_node = entry_xml.convert_root_node(self.__response_xml)
        # __print_xml_children(root)
        tag_head = entry_xml.extract_tag_head(root_node)

        blog_entries = list(filter(lambda blog_entry: blog_entry is not None,
                                   map(lambda entry_node: self.__blog_entry_xmf_parser.parse(
                                       entry_node, tag_head, self.__exclude_entry_ids),
                                       root_node.iter(tag_head + 'entry'))))
        # for entry_node in root_node.iter(tag_head + 'entry'):
        #     # __print_xml_children(entry)
        #     blog_entry = blog_entry_xml.parse(entry_node, tag_head, exclude_ids)
        #     if blog_entry is not None:
        #         blog_entries.add_entry(blog_entry)
        return blog_entries


# Todo: refactor
class BlogEntryResponseBody:
    def __init__(self, hatena_id: str, response_xml: Optional[str]):
        self.__hatena_id = hatena_id
        self.__response_xml = response_xml
        self.__exclude_entry_ids = config.read_lines(EXCLUDE_ENTRY_IDS_TXT_PATH)
        self.__blog_entry_xml_parser = BlogEntryXmlParser(hatena_id)

    def parse(self) -> Optional[PostedBlogEntry]:
        if self.__response_xml is None:
            return None
        root_node = entry_xml.convert_root_node(self.__response_xml)
        tag_head = entry_xml.extract_tag_head(root_node, 'entry')
        return self.__blog_entry_xml_parser.parse(root_node, tag_head, [])
