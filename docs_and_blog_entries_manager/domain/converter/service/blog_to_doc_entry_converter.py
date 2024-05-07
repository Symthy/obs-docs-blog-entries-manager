from typing import Optional

from common.constants import DOCS_DIR_PATH
from domain.blogs.entity.blog_entry import BlogEntry
from domain.docs import DocEntry
from domain.docs.entity.factory.doc_entry_builder import DocEntryBuilder
from domain.docs.value import DocEntryId
from domain.store.datasources.stored_entry_accessor import StoredEntryAccessor
from domain.store.entity.blog_to_doc_entry_mapping import BlogToDocEntryMapping
from files import file_system


class BlogToDocEntryConverter:
    def __init__(self, blog_to_doc_entry_mapping: BlogToDocEntryMapping,
                 stored_doc_entry_accessor: StoredEntryAccessor[DocEntry, DocEntryId]):
        self.__blog_to_doc_entry_mapping = blog_to_doc_entry_mapping
        self.__stored_doc_entry_accessor = stored_doc_entry_accessor

    def convert_to_new(self, blog_entry: BlogEntry, doc_id: DocEntryId):
        builder = DocEntryBuilder()
        builder.id(doc_id)
        builder.title(blog_entry.title)
        builder.dir_path(file_system.join_path(DOCS_DIR_PATH, blog_entry.category_path.value))
        builder.doc_file_name(f'{blog_entry.title}.md')  # Todo: Windowsで使えない文字変換
        builder.category_path(blog_entry.category_path)
        builder.categories(blog_entry.categories)
        builder.updated_at(blog_entry.updated_at)
        return builder.build()

    def convert_to_existing(self, blog_entry: BlogEntry) -> Optional[DocEntry]:
        doc_id: Optional[DocEntryId] = self.__blog_to_doc_entry_mapping.find_doc_entry_id(blog_entry.id)
        if doc_id is None:
            return None

        existed_doc_entry: DocEntry = self.__stored_doc_entry_accessor.load_entry(doc_id)
        if blog_entry.updated_at.is_time_after(existed_doc_entry.updated_at):
            builder = DocEntryBuilder(existed_doc_entry)
            builder.title(blog_entry.title)
            builder.dir_path(file_system.join_path(DOCS_DIR_PATH, blog_entry.category_path.value))
            builder.doc_file_name(f'{blog_entry.title}.md')  # Todo: Windowsで使えない文字変換
            builder.category_path(blog_entry.category_path)
            builder.categories(blog_entry.categories)
            builder.updated_at(blog_entry.updated_at)
            return builder.build()
        return existed_doc_entry
