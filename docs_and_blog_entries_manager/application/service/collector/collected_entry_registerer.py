from application.service.collector.entry_document_saver import EntryDocumentSaver
from application.service.converter.Intermediate_blog_content import IntermediateBlogContent
from application.service.converter.blog_photos_to_doc_images_converter import BlogPhotosToDocImagesConverter
from application.service.converter.blog_to_doc_content_converter import BlogToDocContentConverter
from domain.blogs.datasource.model.posted_blog_entry import PostedBlogEntry
from domain.docs.datasource.interface import IDocumentSaver
from domain.docs.entity.doc_entry import DocEntry
from domain.docs.entity.image.doc_images import DocImages
from domain.docs.value.doc_content import DocContent


class CollectedEntryRegisterer:
    def __init__(self, blog_photos_to_doc_images_converter: BlogPhotosToDocImagesConverter,
                 blog_to_doc_content_converter: BlogToDocContentConverter,
                 entry_document_saver: EntryDocumentSaver, document_file_saver: IDocumentSaver):
        self.__blog_photos_to_doc_images_converter = blog_photos_to_doc_images_converter
        self.__blog_to_doc_content_converter = blog_to_doc_content_converter
        self.__entry_document_saver = entry_document_saver
        self.__document_file_saver = document_file_saver

    def register(self, posted_blog_entries: list[PostedBlogEntry]):
        if len(posted_blog_entries) == 0:
            return
        blog_content_to_doc_entry: dict[IntermediateBlogContent, DocEntry] = {}
        # 記事のリンクを置換するためには一度全てを保存する必要があるため、リンク置換以外を行って先に保存しておく
        for posted_blog_entry in posted_blog_entries:
            doc_entry_path = posted_blog_entry.category_path.value
            photo_entry_to_doc_image = self.__blog_photos_to_doc_images_converter.convert_to_dict(
                posted_blog_entry.photo_entries, doc_entry_path)
            blog_content = self.__blog_to_doc_content_converter.convert_only_category_and_photo(
                posted_blog_entry, photo_entry_to_doc_image)
            doc_content = DocContent(blog_content.value, doc_entry_path)
            doc_images = DocImages(list(photo_entry_to_doc_image.values()))
            doc_entry = self.__entry_document_saver.save(
                posted_blog_entry.convert_to_blog_entry(), doc_content, doc_images)
            blog_content_to_doc_entry[blog_content] = doc_entry
        # 保存したものに、記事のリンクを置換してから保存し直す
        for blog_content, doc_entry in blog_content_to_doc_entry.items():
            doc_content = self.__blog_to_doc_content_converter.convert_link(
                blog_content, doc_entry.category_path.value)
            self.__document_file_saver.save(doc_entry.category_path.value, doc_entry.title, doc_content)
