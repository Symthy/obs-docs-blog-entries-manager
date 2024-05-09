from typing import Optional, List
from urllib.parse import urlparse, parse_qsl

from docs_and_blog_entries_manager.api.api_client import ApiClient
from domain.blogs.datasource.model.post_blog_entry import PostBlogEntry
from domain.blogs.datasource.model.posted_blog_entry import PostedBlogEntry
from domain.blogs.entity.blog_entry import BlogEntry
from domain.entries.interface import IEntryId
from infrastructure.hatena.api.blog_response_parser import BlogEntryResponseBody, BlogEntriesResponseBody
from infrastructure.hatena.templates import request_formats
from logs.logger import Logger


class BlogEntryRepository:
    def __init__(self, blog_api_client: ApiClient, hatena_id: str, summary_entry_id: IEntryId):
        self.__api_client = blog_api_client
        self.__hatena_id = hatena_id
        self.__summary_entry_id = summary_entry_id

    # Blog
    # GET Blog
    def find_id(self, entry_id: IEntryId) -> Optional[PostedBlogEntry]:
        xml_string_opt = self.__api_client.get(path=entry_id.value)
        return BlogEntryResponseBody(xml_string_opt).parse()

    def all(self) -> List[PostedBlogEntry]:
        next_query_params: Optional[list[tuple]] = None
        blog_entries: List[PostedBlogEntry] = []
        while True:
            xml_string_opt = self.__api_client.get(query_params=next_query_params)
            if xml_string_opt is None:
                break
            blog_entries_xml = BlogEntriesResponseBody(xml_string_opt, self.__summary_entry_id.value)
            blog_entries.extend(blog_entries_xml.parse())
            next_url = blog_entries_xml.next_page_url()
            next_query_params = parse_qsl(urlparse(next_url).query)
            if next_query_params is None:
                break
        return blog_entries

    # POST blog
    def post(self, entry: PostBlogEntry, is_draft: bool,
             is_title_escape: bool) -> Optional[BlogEntry]:
        body = request_formats.build_blog_entry_xml_body(self.__hatena_id, entry, is_draft, is_title_escape)
        Logger.info(f'POST Blog: {entry.title}')
        blog_entry_xml = self.__api_client.post(body)
        return BlogEntryResponseBody(blog_entry_xml).parse()

    # PUT blog
    def put(self, entry: PostBlogEntry, is_draft: bool,
            is_title_escape: bool) -> Optional[BlogEntry]:
        blog_entry_xml = self.__put_entry(entry, is_draft, is_title_escape)
        return BlogEntryResponseBody(blog_entry_xml).parse()

    def put_summary_page(self, blog_summary_entry: PostBlogEntry) -> bool:
        # Todo: argument is blog entry object
        # category = 'Summary'
        # title = request_formats.summary_page_title()
        # content = request_formats.build_blog_summary_entry_content(content)
        entry_xml = self.__put_entry(blog_summary_entry, False, False)
        if entry_xml is None:
            return False
        return True

    def __put_entry(self, entry: PostBlogEntry, is_draft: bool, is_title_escape: bool) -> \
            Optional[str]:
        body = request_formats.build_blog_entry_xml_body(self.__hatena_id, entry, is_draft, is_title_escape)
        Logger.info(f'PUT Blog: {entry.title}')
        return self.__api_client.put(body, entry.id)
