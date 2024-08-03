import re
from typing import Optional

from application.service.converter.blog_photos_to_doc_images_converter import BlogPhotosToDocImagesConverter
from config.blog_config import BlogConfig
from domain.blogs.entity.blog_entry import BlogEntry
from domain.blogs.value.blog_content import BlogContent
from domain.docs.types import StoredDocEntriesLoader
from domain.docs.value.doc_content import DocContent
from infrastructure.store.blog_to_doc_entry_mapping import BlogToDocEntryMapping
from infrastructure.store.stored_entry_title_finder import StoredEntryTitleFinder


class BlogToDocContentConverter:

    def __init__(self, blog_config: BlogConfig,
                 blog_photos_to_doc_images_converter: BlogPhotosToDocImagesConverter,
                 blog_entry_title_finder: StoredEntryTitleFinder[BlogEntry],
                 blog_to_doc_mapping: BlogToDocEntryMapping,
                 doc_entries_loader: StoredDocEntriesLoader):
        blog_url_prefix = f'https://{blog_config.blog_id}/'
        self.__blog_entry_title_regex = fr'\!\[(.*)\]\(({blog_url_prefix}.+)\)'
        self.__blog_photos_to_doc_images_converter = blog_photos_to_doc_images_converter
        self.__blog_entry_title_finder = blog_entry_title_finder
        self.__blog_to_doc_mapping = blog_to_doc_mapping
        self.__doc_entries_loader = doc_entries_loader

    def execute(self, blog_content: BlogContent, doc_entry_path: str) -> Optional[DocContent]:
        blog_entry_title_to_url = self.__extract_linked_entry_title_to_url(blog_content)
        blog_entry_link_to_doc_internal_link = {}
        for title, url in blog_entry_title_to_url.items():
            blog_entry_opt = self.__blog_entry_title_finder.find(title)
            linked_doc_entry_id = self.__blog_to_doc_mapping.find_doc_entry_id(blog_entry_opt.id)
            linked_doc_entry = self.__doc_entries_loader.load_entry(linked_doc_entry_id)
            blog_entry_link = f'[{title}]({url})'
            doc_internal_entry = f'[[{linked_doc_entry.title}]]'
            blog_entry_link_to_doc_internal_link[blog_entry_link] = doc_internal_entry
        return self.__convert_content(blog_content, doc_entry_path, blog_entry_link_to_doc_internal_link)

    def __extract_linked_entry_title_to_url(self, blog_content: BlogContent) -> dict[str, str]:
        matches = re.findall(self.__blog_entry_title_regex, blog_content.value)
        title_to_url = {}
        for blog_entry_title, blog_entry_url in matches:
            title_to_url[blog_entry_title] = blog_entry_url
        return title_to_url

    @staticmethod
    def __convert_content(blog_content: BlogContent, doc_entry_path: str,
                          blog_entry_link_to_doc_internal_link: dict[str, str]) -> DocContent:
        content = blog_content.value
        for blog_entry_link, doc_internal_link in blog_entry_link_to_doc_internal_link:
            content.replace(blog_entry_link, doc_internal_link)
        return DocContent(content, doc_entry_path)
