from typing import Optional

from domain.blogs.datasource.model.post_blog_entry import PostBlogEntry
from domain.blogs.entity.blog_entries import BlogEntries
from domain.blogs.entity.blog_entry import BlogEntry
from domain.blogs.entity.factory.blog_entry_builder import BlogEntryBuilder
from domain.blogs.value.blog_entry_id import BlogEntryId
from domain.docs.datasources.model.document_dataset import DocumentDataset
from domain.docs.entity.doc_entries import DocEntries
from domain.docs.entity.doc_entry import DocEntry
from infrastructure.store.blog_to_doc_entry_mapping import BlogToDocEntryMapping
from infrastructure.store.stored_entry_accessor import StoredEntryAccessor


class DocToBlogEntryConverter:
    def __init__(self, blog_to_doc_entry_mapping: BlogToDocEntryMapping,
                 stored_blog_entry_accessor: StoredEntryAccessor[BlogEntry, BlogEntryId]):
        self.__blog_to_doc_entry_mapping = blog_to_doc_entry_mapping
        self.__stored_blog_entry_accessor = stored_blog_entry_accessor

    def convert_bulk_entries(self, doc_entries: DocEntries) -> BlogEntries:
        blog_entries = list(map(lambda blog_entry: self.convert(blog_entry), doc_entries.items))
        return BlogEntries(blog_entries)

    def convert(self, doc_entry: DocEntry) -> BlogEntry:
        blog_id: Optional[BlogEntryId] = self.__blog_to_doc_entry_mapping.find_blog_entry_id(doc_entry.id)
        if blog_id is None:
            builder = BlogEntryBuilder()
            builder.title(doc_entry.title)
            builder.updated_at(doc_entry.updated_at)
            builder.category_path(doc_entry.category_path)
            builder.categories(doc_entry.categories)
            # Todo: 画像
            # builder.doc_images(doc_entry.)
            return builder.build()

        existed_blog_entry: BlogEntry = self.__stored_blog_entry_accessor.load_entry(blog_id)
        if doc_entry.updated_at.is_time_after(existed_blog_entry.updated_at):
            builder = BlogEntryBuilder(existed_blog_entry)
            builder.title(doc_entry.title)
            builder.updated_at(doc_entry.updated_at)
            builder.category_path(doc_entry.category_path)
            builder.categories(doc_entry.categories)
            # Todo: 画像
            # builder.doc_images(doc_entry.)
            return builder.build()
        return existed_blog_entry

    @classmethod
    def convert_to_post(cls, doc_dataset: DocumentDataset) -> PostBlogEntry:
        title = doc_dataset.doc_entry.title
        category_path = doc_dataset.doc_entry.category_path
        categories = doc_dataset.doc_entry.categories
        return PostBlogEntry(title, doc_dataset.doc_content.value, category_path, categories,
                             doc_dataset.doc_content.image_paths)
