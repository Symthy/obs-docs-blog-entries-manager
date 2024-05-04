import xml.etree.ElementTree as ET
from datetime import datetime
from typing import List, Optional

from blogs.datasources.model.posted_blog_entry import PostedBlogEntry


def parse(entry_node: ET.Element, tag_head: str, exclude_ids: List[str]) -> Optional[PostedBlogEntry]:
    # id example: tag:blog.hatena.ne.jp,2013:blog-Sympathia-17680117126980108518-13574176438048806685
    # entry id is last sequence
    entry_id = entry_node.find(tag_head + 'id').text.rsplit('-', 1)[1]
    if entry_id in exclude_ids:
        return None

    title = entry_node.find(tag_head + 'title').text
    content = __extract_content(entry_node, tag_head)
    last_update_time = __resolve_last_update_time(entry_node, tag_head)
    url = __extract_link(entry_node, tag_head)
    categories = __extract_categories(entry_node, tag_head)  # 必ずカテゴリが１つは付与されている
    return PostedBlogEntry(entry_id, title, content, url, last_update_time, categories[0], categories[1:])


def __extract_content(entry_node, tag_head) -> str:
    for cont in entry_node.iter(tag_head + 'content'):
        if cont.attrib['type'] == 'text/x-markdown':
            return cont.text
    return ''


def __resolve_last_update_time(entry_node, tag_head) -> datetime:
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


def __extract_link(entry_node, tag_head) -> str:
    for link in entry_node.iter(tag_head + 'link'):
        if link.attrib['rel'] == 'alternate':
            return link.attrib['href']
    return ''
    # api_url = ''
    # for link in entry_node.iter(tag_head + 'link'):
    #     if link.attrib['rel'] == 'edit':
    #         api_url = link.attrib['href']
    #         break


def __extract_categories(entry_node, tag_head) -> List[str]:
    categories = list(map(lambda category: category.attrib['term'], entry_node.iter(tag_head + 'category')))
    return categories
