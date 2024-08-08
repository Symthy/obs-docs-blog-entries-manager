from application.service.collector.entry_document_saver import EntryDocumentSaver
from application.service.converter.blog_photos_to_doc_images_converter import BlogPhotosToDocImagesConverter
from application.service.converter.blog_to_doc_content_converter import BlogToDocContentConverter
from domain.blogs.datasource.model.posted_blog_entry import PostedBlogEntry
from domain.docs.entity.doc_entry import DocEntry
from infrastructure.documents.document_file_mover import DocumentFileMover


class CollectedEntryUpdater:
    def __init__(self, blog_photos_to_doc_images_converter: BlogPhotosToDocImagesConverter,
                 blog_to_doc_content_converter: BlogToDocContentConverter,
                 entry_document_saver: EntryDocumentSaver, document_file_mover: DocumentFileMover):
        self.__blog_photos_to_doc_images_converter = blog_photos_to_doc_images_converter
        self.__blog_to_doc_content_converter = blog_to_doc_content_converter
        self.__entry_document_saver = entry_document_saver
        self.__document_file_mover = document_file_mover

    def update(self, posted_blog_entry_to_doc_entry: dict[PostedBlogEntry, DocEntry]):
        if len(posted_blog_entry_to_doc_entry) == 0:
            return
        for posted_blog_entry, doc_entry in posted_blog_entry_to_doc_entry.items():
            if posted_blog_entry.updated_at <= doc_entry.updated_at:
                return
            photo_entry_to_doc_image = self.__blog_photos_to_doc_images_converter.convert_to_dict(
                posted_blog_entry.photo_entries, posted_blog_entry.category_path.value)
            doc_content = self.__blog_to_doc_content_converter.convert(
                posted_blog_entry, posted_blog_entry.category_path.value, photo_entry_to_doc_image)
            updated_doc_entry = self.__entry_document_saver.save(posted_blog_entry.convert_to_blog_entry(), doc_content)
            if posted_blog_entry.category_path != doc_entry.category_path.value:
                self.__document_file_mover.move(doc_entry.doc_file_path, updated_doc_entry)
