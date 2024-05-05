from typing import Optional

from blogs.entity.blog_entries import BlogEntries
from blogs.entity.blog_entry import BlogEntry
from blogs.entity.factory.blog_entry_builder import BlogEntryBuilder
from blogs.value.blog_entry_id import BlogEntryId
from docs.entity.doc_entries import DocEntries
from docs.entity.doc_entry import DocEntry
from store.datasources.stored_entry_accessor import StoredEntryAccessor
from store.entity.blog_to_doc_entry_mapping import BlogToDocEntryMapping


class BlogToDocEntryConverter:
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
            builder.original_doc_id(doc_entry.id.value)
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
            builder.original_doc_id(doc_entry.id.value)
            return builder.build()
        return existed_blog_entry
