from typing import Optional, List

from blogs.datasources.hatena.api.xml import entry_xml
from blogs.datasources.model.posted_blog_entry import PostedBlogEntry
from docs_and_blog_entries_manager.blogs.datasources.hatena.api.xml import blog_entry_xml
from docs_and_blog_entries_manager.common.constants import EXCLUDE_ENTRY_IDS_TXT_PATH
from docs_and_blog_entries_manager.files import config


# def __print_xml_children(root: ET.Element):
#     """
#     for debug
#     """
#     for child in root:
#         print(child.tag)

# Todo: refactor (xmlはクラス化して隔離した方が良い)
class BlogEntriesResponseBody:
    def __init__(self, response_xml: str, summary_entry_id: str):
        self.__response_xml = response_xml
        self.__exclude_entry_ids = config.read_lines(EXCLUDE_ENTRY_IDS_TXT_PATH)
        self.__exclude_entry_ids.append(summary_entry_id)  # exclude summary entry index page

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
                                   map(lambda entry_node: blog_entry_xml.parse(entry_node, tag_head,
                                                                               self.__exclude_entry_ids),
                                       root_node.iter(tag_head + 'entry'))))
        # for entry_node in root_node.iter(tag_head + 'entry'):
        #     # __print_xml_children(entry)
        #     blog_entry = blog_entry_xml.parse(entry_node, tag_head, exclude_ids)
        #     if blog_entry is not None:
        #         blog_entries.add_entry(blog_entry)
        return blog_entries


# Todo: refactor
class BlogEntryResponseBody:
    def __init__(self, response_xml: Optional[str]):
        self.__response_xml = response_xml
        self.__exclude_entry_ids = config.read_lines(EXCLUDE_ENTRY_IDS_TXT_PATH)

    def parse(self) -> Optional[PostedBlogEntry]:
        if self.__response_xml is None:
            return None
        root_node = entry_xml.convert_root_node(self.__response_xml)
        tag_head = entry_xml.extract_tag_head(root_node, 'entry')
        return blog_entry_xml.parse(root_node, tag_head, [])
