import xml.etree.ElementTree as ET
from datetime import datetime
from typing import Optional

from blogs.domain.entity import PostedBlogEntry
from blogs.domain.value import BlogEntryId
from blogs.infrastructure.hatena.api.xml import entry_xml


class BlogEntryXmlParser:
    def __init__(self, hatena_id: str):
        self.__hatena_id = hatena_id

    @classmethod
    def extract_next_page_url(cls, response_xml) -> Optional[str]:
        root_node = entry_xml.convert_root_node(response_xml)
        for link in root_node.iter(entry_xml.extract_tag_head(root_node) + 'link'):
            if link.attrib['rel'] == 'next':
                url = link.attrib['href']
                return url
        return None

    def parse_all(self, response_xml: str) -> list[PostedBlogEntry]:
        root_node = entry_xml.convert_root_node(response_xml)
        tag_head = entry_xml.extract_tag_head(root_node)
        return list(
            filter(lambda blog_entry: blog_entry is not None,
                   map(lambda entry_node: self.__parse(entry_node, tag_head),
                       root_node.iter(tag_head + 'entry'))))

    def parse(self, response_xml: str) -> PostedBlogEntry:
        root_node = entry_xml.convert_root_node(response_xml)
        tag_head = entry_xml.extract_tag_head(root_node, 'entry')
        return self.__parse(root_node, tag_head)

    def __parse(self, entry_node: ET.Element, tag_head: str) -> Optional[PostedBlogEntry]:
        # id example: tag:blog.hatena.ne.jp,2013:blog-Sympathia-17680117126980108518-13574176438048806685
        # entry id is last sequence
        entry_id = entry_node.find(tag_head + 'id').text.rsplit('-', 1)[1]

        title = entry_node.find(tag_head + 'title').text
        content = self.__extract_content(entry_node, tag_head)
        last_update_time = self.__resolve_last_update_time(entry_node, tag_head)
        url = self.__extract_link(entry_node, tag_head)
        categories = self.__extract_categories(entry_node, tag_head)  # 必ずカテゴリが１つは付与されている
        return PostedBlogEntry(self.__hatena_id, BlogEntryId(entry_id), title, content, url, last_update_time,
                               categories)

    @classmethod
    def __extract_content(cls, entry_node, tag_head) -> str:
        for content in entry_node.iter(tag_head + 'content'):
            if content.attrib['type'] == 'text/x-markdown':
                return content.text
        return ''

    @classmethod
    def __resolve_last_update_time(cls, entry_node, tag_head) -> datetime:
        updated_opt = entry_node.find(tag_head + 'updated')
        last_update_time = None
        if updated_opt is not None:
            # format: 2013-09-02T11:28:23+09:00
            last_update_time = datetime.strptime(updated_opt.text, "%Y-%m-%dT%H:%M:%S%z")
        app_edited_opt = entry_node.find('{http://www.w3.org/2007/app}edited')  # app:edited
        if app_edited_opt is not None:
            # format: 2013-09-02T11:28:23+09:00
            app_edited_time = datetime.strptime(app_edited_opt.text, "%Y-%m-%dT%H:%M:%S%z")
            if last_update_time < app_edited_time:
                last_update_time = app_edited_time
        return last_update_time

    @classmethod
    def __extract_link(cls, entry_node, tag_head) -> str:
        for link in entry_node.iter(tag_head + 'link'):
            if link.attrib['rel'] == 'alternate':
                return link.attrib['href']
        return ''
        # api_url = ''
        # for link in entry_node.iter(tag_head + 'link'):
        #     if link.attrib['rel'] == 'edit':
        #         api_url = link.attrib['href']
        #         break

    @classmethod
    def __extract_categories(cls, entry_node, tag_head) -> list[str]:
        categories = list(map(lambda category: category.attrib['term'], entry_node.iter(tag_head + 'category')))
        return categories
