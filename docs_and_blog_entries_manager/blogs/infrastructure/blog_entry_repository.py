from typing import Optional
from urllib.parse import urlparse, parse_qsl

from blogs.domain.datasource.interface import IBlogEntryRepository
from blogs.domain.entity import PostedBlogEntry
from blogs.domain.entity import PrePostBlogEntry
from blogs.domain.value import BlogEntryId
from blogs.infrastructure.exceptions.blog_entry_delete_failed_exception import BlogEntryDeleteFailedException
from blogs.infrastructure.exceptions.blog_entry_find_all_failed_exception import BlogEntryFindAllFailedException
from blogs.infrastructure.exceptions.blog_entry_find_failed_exception import BlogEntryFindFailedException
from blogs.infrastructure.exceptions.blog_entry_update_failed_exception import BlogEntryUpdateFailedException
from blogs.infrastructure.hatena.api import BlogApiClient
from blogs.infrastructure.hatena.api import BlogEntryResponseBody, BlogEntriesResponseBody
from blogs.infrastructure.hatena.templates import request_formats
from common.constants import EXCLUDE_ENTRY_IDS_TXT_PATH
from files import config
from logs.logger import Logger


class BlogEntryRepository(IBlogEntryRepository):
    def __init__(self, blog_api_client: BlogApiClient, hatena_id: str, summary_entry_id: BlogEntryId):
        self.__api_client = blog_api_client
        self.__hatena_id = hatena_id
        self.__summary_entry_id = summary_entry_id
        exclude_entry_ids = config.read_lines(EXCLUDE_ENTRY_IDS_TXT_PATH)
        exclude_entry_ids.append(summary_entry_id.value)  # exclude summary entry index page
        self.__exclude_entry_ids = exclude_entry_ids

    # public for Debug
    def get_entry_xml_by_id(self, entry_id: BlogEntryId) -> str:
        return self.__api_client.get(path=entry_id.value)

    # GET Blog
    def find(self, entry_id: BlogEntryId) -> Optional[PostedBlogEntry]:
        try:
            xml_string_opt = self.__api_client.get(path=entry_id.value)
            if xml_string_opt is None:
                raise Exception(f'Not found entry: {entry_id}')
            return BlogEntryResponseBody(self.__hatena_id, xml_string_opt).parse()
        except Exception as e:
            raise BlogEntryFindFailedException(entry_id, e)

    def find_all(self) -> list[PostedBlogEntry]:
        next_query_params: Optional[list[tuple]] = None
        blog_entries: list[PostedBlogEntry] = []
        try:
            while True:
                xml_string_opt = self.__api_client.get(query_params=next_query_params)
                if xml_string_opt is None:
                    break
                blog_entries_xml = BlogEntriesResponseBody(xml_string_opt, self.__hatena_id)
                found_posted_blog_entries = blog_entries_xml.parse()
                filtered_posted_blog_entries = list(
                    filter(lambda entry: entry.id.value not in self.__exclude_entry_ids, found_posted_blog_entries))
                blog_entries.extend(filtered_posted_blog_entries)
                next_url = blog_entries_xml.next_page_url()
                next_query_params = parse_qsl(urlparse(next_url).query)
                if next_query_params is None:
                    break
        except Exception as e:
            raise BlogEntryFindAllFailedException(e)
        return blog_entries

    # POST blog
    def create(self, entry: PrePostBlogEntry, is_draft: bool = False, is_title_escape: bool = True) -> PostedBlogEntry:
        body = request_formats.build_blog_entry_xml_body(self.__hatena_id, entry, is_draft, is_title_escape)
        Logger.info(f'POST Blog: {entry.title}')
        blog_entry_xml = self.__api_client.post(body)
        return BlogEntryResponseBody(self.__hatena_id, blog_entry_xml).parse()

    # PUT blog
    def update(self, entry_id: BlogEntryId, entry: PrePostBlogEntry, is_draft: bool = False,
               is_title_escape: bool = True) -> PostedBlogEntry:
        try:
            blog_entry_xml = self.__update_entry(entry_id, entry, is_draft, is_title_escape)
            return BlogEntryResponseBody(self.__hatena_id, blog_entry_xml).parse()
        except Exception as e:
            raise BlogEntryUpdateFailedException(entry_id, e)

    def update_summary(self, entry_id: BlogEntryId, blog_summary_entry: PrePostBlogEntry) -> bool:
        # summary は blog entry をローカルに保存しない
        # category = 'Summary'
        # title = request_formats.summary_page_title()
        # content = request_formats.build_blog_summary_entry_content(content)
        entry_xml_opt = self.__update_entry(entry_id, blog_summary_entry)
        if entry_xml_opt is None:
            return False
        return True

    def __update_entry(self, entry_id: BlogEntryId, entry: PrePostBlogEntry, is_draft: bool = False,
                       is_title_escape: bool = True) -> Optional[str]:
        body = request_formats.build_blog_entry_xml_body(self.__hatena_id, entry, is_draft, is_title_escape)
        Logger.info(f'PUT Blog: {entry.title}')
        return self.__api_client.put(body, entry_id.value)

    def delete(self, entry_id: BlogEntryId):
        try:
            self.__api_client.delete(entry_id.value)
        except Exception as e:
            raise BlogEntryDeleteFailedException(entry_id, e)
