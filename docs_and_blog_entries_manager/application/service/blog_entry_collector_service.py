from typing import List

from application.service.converter.blog_to_doc_entry_converter import BlogToDocEntryConverter
from application.service.converter.photo_entries_to_doc_images_converter import PhotoEntriesToDocImagesConverter
from application.service.store.entry_persistence_service import EntryPersistenceService
from domain.blogs.datasource.model.posted_blog_entry import PostedBlogEntry
from domain.blogs.services.posted_blog_entry_collector import PostedBlogEntryCollector
from domain.docs.entity.doc_entry import DocEntry
from domain.docs.value.doc_content import DocContent
from infrastructure.documents.document_file_accessor import DocumentFileAccessor


class BlogEntryCollectorService:
    def __init__(self,
                 posted_blog_entry_collector: PostedBlogEntryCollector,
                 blog_to_doc_entry_converter: BlogToDocEntryConverter,
                 photo_entries_to_doc_images_converter: PhotoEntriesToDocImagesConverter,
                 entry_persistence_service: EntryPersistenceService,
                 document_file_accessor: DocumentFileAccessor):
        self.__posted_blog_entry_collector = posted_blog_entry_collector
        self.__blog_to_doc_entry_converter = blog_to_doc_entry_converter
        self.__photo_entries_to_doc_images_converter = photo_entries_to_doc_images_converter
        self.__entry_persistence_service = entry_persistence_service
        self.__document_file_accessor = document_file_accessor

    def execute(self):
        posted_blog_entries: List[PostedBlogEntry] = self.__posted_blog_entry_collector.execute()
        self.__save_all(posted_blog_entries)

    def __save_all(self, posted_blog_entries: List[PostedBlogEntry]):
        # Todo: errorケース md保存成功して、json保存失敗したら、mdは残す（他機能で救えるため
        for posted_blog_entry in posted_blog_entries:
            doc_entry_path = posted_blog_entry.category_path.value
            doc_content = DocContent(posted_blog_entry.content.value_with_inserted_categories, doc_entry_path)
            doc_images = self.__photo_entries_to_doc_images_converter.execute(posted_blog_entry.photo_entries,
                                                                              doc_entry_path)
            doc_entry_id = self.__document_file_accessor.save_doc_set(doc_entry_path, posted_blog_entry.title,
                                                                      doc_content, doc_images)
            blog_entry = posted_blog_entry.convert_to_blog_entry()
            doc_entry: DocEntry = self.__blog_to_doc_entry_converter.convert_to_new(blog_entry, doc_entry_id)
            self.__entry_persistence_service.save_entry_data(blog_entry, doc_entry)
