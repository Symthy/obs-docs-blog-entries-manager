from typing import List

from common.constants import DOCS_DIR_PATH
from domain.blogs.datasources.model.posted_blog_entry import PostedBlogEntry
from domain.blogs.entity.blog_entry import BlogEntry
from domain.blogs.services.posted_blog_entry_collector import PostedBlogEntryCollector
from domain.blogs.value.blog_entry_id import BlogEntryId
from domain.converter.service.blog_to_doc_entry_converter import BlogToDocEntryConverter
from domain.converter.service.photo_entries_to_doc_images_converter import PhotoEntriesToDocImagesConverter
from domain.docs.entity.doc_entry import DocEntry
from domain.docs.entity.image.doc_images import DocImages
from domain.docs.value.doc_content import DocContent
from domain.docs.value.doc_entry_id import DocEntryId
from domain.entries.values.entry_date_time import EntryDateTime
from domain.store.datasources.stored_entry_accessor import StoredEntryAccessor
from domain.store.entity.blog_to_doc_entry_mapping import BlogToDocEntryMapping
from files import file_system, text_file, image_file


class DocDataSet:
    def __init__(self, entry: DocEntry, content: DocContent, images: DocImages):
        self.__entry = entry
        self.__content = content
        self.__images = images

    @property
    def entry(self) -> DocEntry:
        return self.__entry

    @property
    def content(self) -> DocContent:
        return self.__content

    @property
    def images(self) -> DocImages:
        return self.__images


# Todo: 責務持たせすぎ。分割
class BlogEntryCollectorService:
    def __init__(self, document_storage_dir_path: str,
                 posted_blog_entry_collector: PostedBlogEntryCollector,
                 blog_to_doc_entry_converter: BlogToDocEntryConverter,
                 photo_entries_to_doc_images_converter: PhotoEntriesToDocImagesConverter,
                 stored_doc_entry_accessor: StoredEntryAccessor[DocEntry, DocEntryId],
                 stored_blog_entry_accessor: StoredEntryAccessor[BlogEntry, BlogEntryId],
                 blog_to_doc_entry_mapping: BlogToDocEntryMapping,
                 docs_dir_path: str = DOCS_DIR_PATH):
        self.__document_storage_dir_path = document_storage_dir_path
        self.__posted_blog_entry_collector = posted_blog_entry_collector
        self.__blog_to_doc_entry_converter = blog_to_doc_entry_converter
        self.__photo_entries_to_doc_images_converter = photo_entries_to_doc_images_converter
        self.__stored_doc_entry_accessor = stored_doc_entry_accessor
        self.__stored_blog_entry_accessor = stored_blog_entry_accessor
        self.__blog_to_doc_entry_mapping = blog_to_doc_entry_mapping
        self.__docs_dir_path = docs_dir_path

    def execute(self):
        posted_blog_entries: List[PostedBlogEntry] = self.__posted_blog_entry_collector.execute()
        self.__save_all(posted_blog_entries)

    def __save_all(self, posted_blog_entries: List[PostedBlogEntry]):
        for posted_blog_entry in posted_blog_entries:
            doc_entry_dir_path = file_system.join_path(self.__document_storage_dir_path,
                                                       posted_blog_entry.category_path.value)
            doc_content = DocContent(posted_blog_entry.content.value_with_inserted_categories, doc_entry_dir_path)
            doc_images = self.__photo_entries_to_doc_images_converter.execute(posted_blog_entry.photo_entries,
                                                                              doc_entry_dir_path)
            doc_entry_id = self.__save_doc_file(doc_entry_dir_path, posted_blog_entry.title, doc_content, doc_images)
            blog_entry = posted_blog_entry.convert_to_blog_entry()
            doc_entry: DocEntry = self.__blog_to_doc_entry_converter.convert_to_new(blog_entry, doc_entry_id)

    def __save_doc_file(self, doc_entry_dir_path: str, title: str, content: DocContent,
                        images: DocImages) -> DocEntryId:
        doc_file_path = file_system.join_path(doc_entry_dir_path, f'{title}.md')
        text_file.write_file(doc_file_path, content.value)
        for image in images.items:
            image_file.write(image.file_path, image.image_data)
        created_date_time = file_system.get_created_file_time(doc_file_path)
        return self.__build_doc_id(EntryDateTime(created_date_time))

    @staticmethod
    def __build_doc_id(created_date_time: EntryDateTime) -> DocEntryId:
        return DocEntryId(created_date_time.to_str_with_num_sequence())

    def __save_entry_data(self, blog_entry: BlogEntry, doc_entry: DocEntry):
        self.__stored_doc_entry_accessor.save_entry(doc_entry)
        self.__stored_blog_entry_accessor.save_entry(blog_entry)
        self.__blog_to_doc_entry_mapping.push_entry_pair(blog_entry.id, doc_entry.id)
