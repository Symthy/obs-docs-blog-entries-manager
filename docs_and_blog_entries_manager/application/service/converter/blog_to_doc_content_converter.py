import re

from application.service.converter.Intermediate_blog_content import IntermediateBlogContent
from domain.blogs.datasource.model.posted_blog_entry import PostedBlogEntry
from domain.blogs.entity.blog_entry import BlogEntry
from domain.blogs.entity.photo.photo_entry import PhotoEntry
from domain.blogs.value.blog_content import BlogContent
from domain.docs.entity.image.doc_image import DocImage
from domain.docs.types import StoredDocEntriesLoader
from domain.docs.value.doc_content import DocContent
from infrastructure.store.blog_to_doc_entry_mapping import BlogToDocEntryMapping
from infrastructure.store.stored_entry_title_finder import StoredEntryTitleFinder


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

    def convert(self, posted_blog_entry: PostedBlogEntry, doc_entry_path: str,
                photo_entry_to_doc_image: dict[PhotoEntry, DocImage]) -> DocContent:
        blog_content = self.__convert_only_category_and_photo(posted_blog_entry, photo_entry_to_doc_image)
        return self.convert_link(blog_content, doc_entry_path)

    def convert_link(self, blog_content: IntermediateBlogContent, doc_entry_path: str) -> DocContent:
        blog_entry_title_to_url = self.__extract_linked_entry_title_to_url(blog_content)
        blog_entry_link_to_doc_internal_link = {}
        for title, url in blog_entry_title_to_url.items():
            blog_entry_opt = self.__blog_entry_title_finder.find(title)
            linked_doc_entry_id = self.__blog_to_doc_mapping.find_doc_entry_id(blog_entry_opt.id)
            linked_doc_entry = self.__stored_doc_entries_loader.load_entry(linked_doc_entry_id)
            blog_entry_link = f'[{title}]({url})'
            doc_internal_entry = f'[[{linked_doc_entry.title}]]'
            blog_entry_link_to_doc_internal_link[blog_entry_link] = doc_internal_entry
        return self.__convert_content(blog_content, doc_entry_path, blog_entry_link_to_doc_internal_link)

    @classmethod
    def convert_for_register(cls, posted_blog_entry: PostedBlogEntry,
                             photo_entry_to_doc_image: dict[PhotoEntry, DocImage]) \
            -> tuple[DocContent, IntermediateBlogContent]:
        blog_content: IntermediateBlogContent = cls.__convert_only_category_and_photo(
            posted_blog_entry, photo_entry_to_doc_image)
        doc_content = DocContent(blog_content.value, posted_blog_entry.category_path.value)
        return doc_content, blog_content

    @staticmethod
    def __convert_content(blog_content: BlogContent | IntermediateBlogContent, doc_entry_path: str,
                          blog_entry_link_to_doc_internal_link: dict[str, str]) -> DocContent:
        content = blog_content.value
        for blog_entry_link, doc_internal_link in blog_entry_link_to_doc_internal_link.items():
            content = content.replace(blog_entry_link, doc_internal_link)
        return DocContent(content, doc_entry_path)

    @staticmethod
    def __convert_only_category_and_photo(
            posted_blog_entry: PostedBlogEntry, photo_entry_to_doc_image: dict[PhotoEntry, DocImage]) \
            -> IntermediateBlogContent:
        blog_content = posted_blog_entry.content.value_with_inserted_categories
        for photo_entry, doc_image in photo_entry_to_doc_image.items():
            blog_content.replace_photo_link(photo_entry.id, doc_image.file_link)
        return IntermediateBlogContent(blog_content)

    def __extract_linked_entry_title_to_url(self, blog_content: BlogContent | IntermediateBlogContent) \
            -> dict[str, str]:
        matches = re.findall(self.__blog_entry_link_regex, blog_content.value)
        title_to_url = {}
        for blog_entry_title, blog_entry_url in matches:
            title_to_url[blog_entry_title] = blog_entry_url
        return title_to_url
