import re

from blogs.domain.datasource.model import PostedBlogEntry
from blogs.domain.entity import PhotoEntry
from blogs.domain.entity.blog_entry import BlogEntry
from blogs.domain.value import BlogContent
from composites.converter.Intermediate_blog_content import _IntermediateBlogContent
from composites.entity import BlogToDocEntryMapping
from docs.domain.datasource.interface import StoredDocEntriesLoader
from docs.domain.value import DocContent
from docs.domain.value import DocImage
from stores.infrastructure import StoredEntryTitleFinder


class BlogToDocContentConverter:

    def __init__(self, blog_id: str,
                 blog_entry_title_finder: StoredEntryTitleFinder[BlogEntry],
                 blog_to_doc_mapping: BlogToDocEntryMapping,
                 stored_doc_entries_loader: StoredDocEntriesLoader):
        blog_url_prefix = f'https://{blog_id}/'
        self.__blog_entry_link_regex = fr'\[(.*)\]\(({blog_url_prefix}.+)\)'
        self.__blog_entry_title_finder = blog_entry_title_finder
        self.__blog_to_doc_mapping = blog_to_doc_mapping
        self.__stored_doc_entries_loader = stored_doc_entries_loader

    def convert(self, posted_blog_entry: PostedBlogEntry,
                photo_entry_to_doc_image: dict[PhotoEntry, DocImage]) -> DocContent:
        blog_content = self.convert_only_category_and_photo(posted_blog_entry, photo_entry_to_doc_image)
        return self.convert_link(blog_content)

    def convert_link(self, blog_content: _IntermediateBlogContent) -> DocContent:
        blog_entry_title_to_url = self.__extract_linked_entry_title_to_url(blog_content)
        blog_entry_link_to_doc_internal_link = {}
        for title, url in blog_entry_title_to_url.items():
            blog_entry_opt = self.__blog_entry_title_finder.find(title)
            linked_doc_entry_id = self.__blog_to_doc_mapping.find_doc_entry_id(blog_entry_opt.id)
            linked_doc_entry = self.__stored_doc_entries_loader.load_entry(linked_doc_entry_id)
            blog_entry_link = f'[{title}]({url})'
            doc_internal_entry = f'[[{linked_doc_entry.title}]]'
            blog_entry_link_to_doc_internal_link[blog_entry_link] = doc_internal_entry
        return self.__convert_content(blog_content, blog_entry_link_to_doc_internal_link)

    @staticmethod
    def __convert_content(blog_content: BlogContent | _IntermediateBlogContent,
                          blog_entry_link_to_doc_internal_link: dict[str, str]) -> DocContent:
        content = blog_content.value
        for blog_entry_link, doc_internal_link in blog_entry_link_to_doc_internal_link.items():
            content = content.replace(blog_entry_link, doc_internal_link)
        return DocContent(content)

    @classmethod
    def convert_only_category_and_photo(
            cls, posted_blog_entry: PostedBlogEntry,
            photo_entry_to_doc_image: dict[PhotoEntry, DocImage]) -> _IntermediateBlogContent:
        blog_content = posted_blog_entry.content.value_with_inserted_categories
        for photo_entry, doc_image in photo_entry_to_doc_image.items():
            blog_content.replace_photo_link(photo_entry.id, doc_image.file_link)
        return _IntermediateBlogContent(blog_content)

    def __extract_linked_entry_title_to_url(self, blog_content: BlogContent | _IntermediateBlogContent) \
            -> dict[str, str]:
        matches = re.findall(self.__blog_entry_link_regex, blog_content.value)
        title_to_url = {}
        for blog_entry_title, blog_entry_url in matches:
            title_to_url[blog_entry_title] = blog_entry_url
        return title_to_url
