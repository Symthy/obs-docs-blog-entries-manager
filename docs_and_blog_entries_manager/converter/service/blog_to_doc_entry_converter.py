from typing import Optional

from blogs.entity.blog_entries import BlogEntries
from blogs.entity.blog_entry import BlogEntry
from common.constants import DOCS_DIR_PATH
from docs.entity.doc_entries import DocEntries
from docs.entity.doc_entry import DocEntry
from docs.entity.factory.doc_entry_builder import DocEntryBuilder
from files import file_system
from store.datasources.stored_entry_accessor import StoredEntryAccessor
from store.entity.blog_to_doc_entry_mapping import BlogToDocEntryMapping


class BlogToDocEntryConverter:
    def __init__(self, blog_to_doc_entry_mapping: BlogToDocEntryMapping,
                 stored_doc_entry_accessor: StoredEntryAccessor[DocEntry]):
        self.__blog_to_doc_entry_mapping = blog_to_doc_entry_mapping
        self.__stored_doc_entry_accessor = stored_doc_entry_accessor

    def convert_bulk_entries(self, blog_entries: BlogEntries) -> DocEntries:
        doc_entries = list(map(lambda blog_entry: self.convert(blog_entry), blog_entries.items))
        return DocEntries(doc_entries)

    def convert(self, blog_entry: BlogEntry) -> DocEntry:
        doc_id: Optional[str] = self.__blog_to_doc_entry_mapping.find_doc_entry_id(blog_entry.id)
        if doc_id is None:
            builder = DocEntryBuilder()
            builder.title(blog_entry.title)
            builder.dir_path(file_system.join_path(DOCS_DIR_PATH, blog_entry.category_path.value))
            builder.doc_file_name(f'{blog_entry.title}.md')  # Todo: Windowsで使えない文字変換
            builder.category_path(blog_entry.category_path)
            builder.categories(blog_entry.categories)
            builder.pickup(False)
            return builder.build()

        old_doc_entry: DocEntry = self.__stored_doc_entry_accessor.load_entry(doc_id)
        if blog_entry.updated_at.is_time_after(old_doc_entry.updated_at):
            builder = DocEntryBuilder(old_doc_entry)
            builder.title(blog_entry.title)
            builder.dir_path(file_system.join_path(DOCS_DIR_PATH, blog_entry.category_path.value))
            builder.doc_file_name(f'{blog_entry.title}.md')  # Todo: Windowsで使えない文字変換
            builder.category_path(blog_entry.category_path)
            builder.categories(blog_entry.categories)
            builder.updated_at(blog_entry.updated_at)
            return builder.build()
        return old_doc_entry
