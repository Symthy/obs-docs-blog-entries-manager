from typing import Optional

from application.service.converter.blog_photos_to_doc_images_converter import BlogPhotosToDocImagesConverter
from application.service.converter.blog_to_doc_content_converter import BlogToDocContentConverter
from common.constants import BLOG_CATEGORY
from domain.blogs.datasource.model.posted_blog_entry import PostedBlogEntry
from domain.blogs.entity.blog_entry import BlogEntry
from domain.docs.datasources.model.document_dataset import DocumentDataset
from domain.docs.entity.doc_entry import DocEntry
from domain.docs.entity.factory.doc_entry_builder import DocEntryBuilder
from domain.docs.value.doc_entry_id import DocEntryId
from infrastructure.store.blog_to_doc_entry_mapping import BlogToDocEntryMapping
from infrastructure.types import StoredDocEntriesAccessor


class BlogToDocEntryConverter:
    def __init__(self, blog_to_doc_entry_mapping: BlogToDocEntryMapping,
                 stored_doc_entries_accessor: StoredDocEntriesAccessor,
                 blog_photos_to_doc_images_converter: BlogPhotosToDocImagesConverter,
                 blog_to_doc_content_converter: BlogToDocContentConverter):
        self.__blog_to_doc_entry_mapping = blog_to_doc_entry_mapping
        self.__stored_doc_entries_accessor = stored_doc_entries_accessor
        self.__blog_photos_to_doc_images_converter = blog_photos_to_doc_images_converter
        self.__blog_to_doc_content_converter = blog_to_doc_content_converter

    def convert(self, posted_blog_entry: PostedBlogEntry) -> DocumentDataset:
        doc_entry_path = posted_blog_entry.category_path.value
        blog_entry = posted_blog_entry.convert_to_blog_entry()
        doc_entry_id = self.__blog_to_doc_entry_mapping.find_doc_entry_id(blog_entry.id)
        doc_content = self.__blog_to_doc_content_converter.convert(posted_blog_entry.content, doc_entry_path)
        doc_entry = self.convert_to_doc_entry(blog_entry, doc_entry_id)
        return DocumentDataset(doc_entry, doc_content)

    def convert_to_doc_entry(self, blog_entry: BlogEntry, doc_id: DocEntryId) -> Optional[DocEntry]:
        if not self.__blog_to_doc_entry_mapping.exist(blog_entry.id):
            self.__convert_to_new(blog_entry, doc_id)
            return
        self.__convert_to_existing(blog_entry)

    @staticmethod
    def __convert_to_new(blog_entry: BlogEntry, doc_id: DocEntryId) -> DocEntry:
        builder = DocEntryBuilder()
        builder.id(doc_id)
        builder.title(blog_entry.title)
        builder.doc_file_name(f'{blog_entry.title}.md')  # Todo: Windowsで使えない文字変換
        builder.category_path(blog_entry.category_path)
        builder.categories(*blog_entry.categories, BLOG_CATEGORY)
        builder.updated_at(blog_entry.updated_at)
        return builder.build()

    def __convert_to_existing(self, blog_entry: BlogEntry) -> Optional[DocEntry]:
        doc_id: Optional[DocEntryId] = self.__blog_to_doc_entry_mapping.find_doc_entry_id(blog_entry.id)
        if doc_id is None:
            return None
        existed_doc_entry: DocEntry = self.__stored_doc_entries_accessor.load_entry(doc_id)
        if blog_entry.updated_at.is_time_after(existed_doc_entry.updated_at):
            builder = DocEntryBuilder(existed_doc_entry)
            builder.title(blog_entry.title)
            builder.doc_file_name(f'{blog_entry.title}.md')  # Todo: Windowsで使えない文字変換
            builder.category_path(blog_entry.category_path)
            builder.categories(*blog_entry.categories, BLOG_CATEGORY)
            builder.updated_at(blog_entry.updated_at)
            return builder.build()
        return existed_doc_entry
