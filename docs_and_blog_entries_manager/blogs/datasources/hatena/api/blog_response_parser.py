from typing import Optional

from docs_and_blog_entries_manager.blogs.datasources.hatena.api.xml import blog_entry_xml
from docs_and_blog_entries_manager.blogs.entity.blog_entries import BlogEntries
from docs_and_blog_entries_manager.blogs.entity.blog_entry import BlogEntry
from docs_and_blog_entries_manager.common.constants import EXCLUDE_ENTRY_IDS_TXT_PATH
from docs_and_blog_entries_manager.files import config


# def __print_xml_children(root: ET.Element):
#     """
#     for debug
#     """
#     for child in root:
#         print(child.tag)

# Todo: refactor
class BlogEntriesResponseBody:
    def __init__(self, response_xml: str):
        self.__response_xml = response_xml

    def next_page_url(self) -> Optional[str]:
        url = None
        root_node = blog_entry_xml.convert_root_node(self.__response_xml)
        for link in root_node.iter(blog_entry_xml.extract_tag_head(root_node) + 'link'):
            if link.attrib['rel'] == 'next':
                url = link.attrib['href']
                break
        return url

    def parse(self, summary_entry_id: str) -> BlogEntries:
        root_node = blog_entry_xml.convert_root_node(self.__response_xml)
        # __print_xml_children(root)
        tag_head = blog_entry_xml.extract_tag_head(root_node)
        exclude_ids = config.read_lines(EXCLUDE_ENTRY_IDS_TXT_PATH)
        exclude_ids.append(summary_entry_id)  # exclude summary entry index page

        blog_entries = list(filter(lambda blog_entry: blog_entry is not None,
                                   map(lambda entry_node: blog_entry_xml.parse(entry_node, tag_head, exclude_ids),
                                       root_node.iter(tag_head + 'entry'))))
        # for entry_node in root_node.iter(tag_head + 'entry'):
        #     # __print_xml_children(entry)
        #     blog_entry = blog_entry_xml.parse(entry_node, tag_head, exclude_ids)
        #     if blog_entry is not None:
        #         blog_entries.add_entry(blog_entry)
        return BlogEntries(blog_entries)


# Todo: refactor
class BlogEntryResponseBody:
    def __init__(self, response_xml: Optional[str]):
        self.__response_xml = response_xml

    def parse(self) -> Optional[BlogEntry]:
        if self.__response_xml is None:
            return None
        root_node = blog_entry_xml.convert_root_node(self.__response_xml)
        tag_head = blog_entry_xml.extract_tag_head(root_node, 'entry')
        return blog_entry_xml.parse(root_node, tag_head, [])
