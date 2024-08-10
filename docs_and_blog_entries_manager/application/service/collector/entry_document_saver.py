from application.service.converter.blog_to_doc_entry_converter import BlogToDocEntryConverter
from domain.blogs.datasource.interface import StoredBlogEntriesAccessor
from domain.blogs.entity.blog_entry import BlogEntry
from domain.docs.datasource.interface import IDocumentSaver, StoredDocEntriesAccessor
from domain.docs.entity.doc_entry import DocEntry
from domain.docs.entity.image.doc_images import DocImages
from domain.docs.value.doc_content import DocContent
from domain.mappings.blog_to_doc_entry_mapping import BlogToDocEntryMapping


class EntryDocumentSaver:
    def __init__(self, blog_to_doc_entry_mapping: BlogToDocEntryMapping,
                 stored_blog_entries_accessor: StoredBlogEntriesAccessor,
                 stored_doc_entries_accessor: StoredDocEntriesAccessor,
                 document_file_saver: IDocumentSaver,
                 blog_to_doc_entry_converter: BlogToDocEntryConverter):
        self.__blog_to_doc_entry_mapping = blog_to_doc_entry_mapping
        self.__stored_blog_entries_accessor = stored_blog_entries_accessor
        self.__stored_doc_entries_accessor = stored_doc_entries_accessor
        self.__document_file_saver = document_file_saver
        self.__blog_to_doc_entry_converter = blog_to_doc_entry_converter

    def save(self, blog_entry: BlogEntry, doc_content: DocContent,
             doc_images: DocImages | None = None) -> DocEntry:
        doc_entry_id = self.__document_file_saver.save(
            blog_entry.category_path.value, blog_entry.title, doc_content, doc_images)
        doc_entry = self.__blog_to_doc_entry_converter.convert_to_doc_entry(blog_entry, doc_entry_id)
        self.__stored_doc_entries_accessor.save_entry(doc_entry)
        self.__stored_blog_entries_accessor.save_entry(blog_entry)
        self.__blog_to_doc_entry_mapping.push_entry_pair(blog_entry.id, doc_entry.id)
        return doc_entry
