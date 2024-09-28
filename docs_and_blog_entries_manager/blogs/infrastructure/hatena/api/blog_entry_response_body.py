from typing import Optional

from blogs.domain.entity import PostedBlogEntry
from blogs.infrastructure.hatena.api.xml import BlogEntryXmlParser


# def __print_xml_children(root: ET.Element):
#     """
#     for debug
#     """
#     for child in root:
#         print(child.tag)

# Todo: refactor (xmlはクラス化して隔離した方が良い)
class BlogEntriesResponseBody:
    def __init__(self, response_xml: str, hatena_id: str):
        self.__hatena_id = hatena_id
        self.__response_xml = response_xml
        self.__blog_entry_xmf_parser = BlogEntryXmlParser(hatena_id)

    def next_page_url(self) -> Optional[str]:
        return self.__blog_entry_xmf_parser.extract_next_page_url(self.__response_xml)

    def parse(self) -> list[PostedBlogEntry]:
        posted_blog_entries = self.__blog_entry_xmf_parser.parse_all(self.__response_xml)
        # for entry_node in root_node.iter(tag_head + 'entry'):
        #     # __print_xml_children(entry)
        #     blog_entry = blog_entry_xml.parse(entry_node, tag_head, exclude_ids)
        #     if blog_entry is not None:
        #         blog_entries.add_entry(blog_entry)
        return posted_blog_entries


# Todo: refactor
class BlogEntryResponseBody:
    def __init__(self, hatena_id: str, response_xml: str):
        self.__hatena_id = hatena_id
        self.__response_xml = response_xml
        self.__blog_entry_xml_parser = BlogEntryXmlParser(hatena_id)

    def parse(self) -> PostedBlogEntry:
        return self.__blog_entry_xml_parser.parse(self.__response_xml)
