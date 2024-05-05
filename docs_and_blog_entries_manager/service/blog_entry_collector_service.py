from typing import List

from blogs.datasources.hatena.image.image_downloader import ImageDownLoader
from blogs.datasources.model.posted_blog_entry import PostedBlogEntry
from blogs.services.posted_blog_entry_collector import PostedBlogEntryCollector
from converter.service.blog_to_doc_entry_converter import BlogToDocEntryConverter
from docs.entity.doc_entry import DocEntry
from docs.entity.image.doc_image import DocImage
from docs.entity.image.doc_images import DocImages
from docs.value.doc_content import DocContent
from docs.value.doc_entry_id import DocEntryId
from files import file_system, text_file, image_file
from store.datasources.stored_entry_accessor import StoredEntryAccessor


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


class BlogEntryCollectorService:
    def __init__(self, document_storage_dir_path: str,
                 posted_blog_entry_collector: PostedBlogEntryCollector,
                 blog_to_doc_entry_converter: BlogToDocEntryConverter,
                 stored_doc_entry_accessor: StoredEntryAccessor[DocEntry, DocEntryId]):
        self.__document_storage_dir_path = document_storage_dir_path
        self.__posted_blog_entry_collector = posted_blog_entry_collector
        self.__blog_to_doc_entry_converter = blog_to_doc_entry_converter
        self.__stored_doc_entry_accessor = stored_doc_entry_accessor

    def execute(self):
        posted_blog_entries: List[PostedBlogEntry] = self.__posted_blog_entry_collector.execute()
        doc_data_sets: List[DocDataSet] = self.__convert_all(posted_blog_entries)
        self.__save_documents(doc_data_sets)

    def __convert_all(self, posted_blog_entries: List[PostedBlogEntry]) -> List[DocDataSet]:
        return list(map(lambda blog_entry: self.__convert(blog_entry), posted_blog_entries))

    def __convert(self, posted_blog_entry: PostedBlogEntry) -> DocDataSet:
        doc_entry_dir_path = file_system.join_path(self.__document_storage_dir_path,
                                                   posted_blog_entry.category_path.value)
        doc_content = DocContent(posted_blog_entry.content.value_with_inserted_categories, doc_entry_dir_path)
        blog_entry = posted_blog_entry.convert_to_blog_entry()
        doc_entry: DocEntry = self.__blog_to_doc_entry_converter.convert(blog_entry)

        doc_images: List[DocImage] = []
        for blog_image in blog_entry.images.items:
            image_data: bytes = ImageDownLoader.run(blog_image.image_url)
            doc_image = DocImage(doc_entry_dir_path, blog_image.image_filename, image_data)
            doc_images.append(doc_image)
        return DocDataSet(doc_entry, doc_content, DocImages(doc_images))

    def __save_documents(self, doc_data_sets: List[DocDataSet]):
        for doc_data_set in doc_data_sets:
            self.__stored_doc_entry_accessor.save_entry(doc_data_set.entry)
            doc_file_path = doc_data_set.entry.doc_file_path
            text_file.write_file(doc_file_path, doc_data_set.content.value)
            for image in doc_data_set.images.items:
                image_file.write(image.file_path, image.image_data)
