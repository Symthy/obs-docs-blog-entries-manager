from application.service.collector.entry_and_document_saver import EntryAndDocumentSaver
from application.service.converter.Intermediate_blog_content import IntermediateBlogContent
from application.service.converter.blog_photos_to_doc_images_converter import BlogPhotosToDocImagesConverter
from application.service.converter.blog_to_doc_content_converter import BlogToDocContentConverter
from domain.blogs.datasource.interface import IBlogEntryRepository
from domain.blogs.datasource.model.posted_blog_entry import PostedBlogEntry
from domain.docs.entity.doc_entry import DocEntry
from domain.docs.entity.image.doc_images import DocImages
from domain.docs.value.doc_content import DocContent
from infrastructure.documents.document_file_accessor import DocumentFileAccessor
from infrastructure.store.blog_to_doc_entry_mapping import BlogToDocEntryMapping


class BlogEntryCollectorService:
    """
    blogから投稿済み記事を収集し、ローカルに保存する
    """

    def __init__(self,
                 blog_to_doc_entry_mapping: BlogToDocEntryMapping,
                 posted_blog_entry_repository: IBlogEntryRepository,
                 document_file_accessor: DocumentFileAccessor,
                 blog_photos_to_doc_images_converter: BlogPhotosToDocImagesConverter,
                 blog_to_doc_content_converter: BlogToDocContentConverter,
                 entry_and_document_saver: EntryAndDocumentSaver):
        self.__blog_to_doc_entry_mapping = blog_to_doc_entry_mapping
        self.__posted_blog_entry_repository = posted_blog_entry_repository
        self.__document_file_accessor = document_file_accessor
        self.__blog_photos_to_doc_images_converter = blog_photos_to_doc_images_converter
        self.__blog_to_doc_content_converter = blog_to_doc_content_converter
        self.__entry_and_document_saver = entry_and_document_saver

    def execute(self):
        posted_blog_entries: list[PostedBlogEntry] = self.__posted_blog_entry_repository.find_all()
        self.__save_all(posted_blog_entries)

    def __save_all(self, posted_blog_entries: list[PostedBlogEntry]):
        # Todo: errorケース md保存成功して、json保存失敗したら、mdは残す（他機能で救えるため
        new_entries = list(filter(lambda entry: self.__blog_to_doc_entry_mapping.exist(entry.id), posted_blog_entries))
        exist_posted_blog_entry_to_doc_entry = dict(
            filter(lambda blog_entry_to_doc_entry: blog_entry_to_doc_entry[1] is not None,
                   map(lambda blog_entry: (
                       blog_entry, self.__blog_to_doc_entry_mapping.find_doc_entry_id(blog_entry.id)),
                       posted_blog_entries)))
        self.__register_local(new_entries)
        self.__update_local(exist_posted_blog_entry_to_doc_entry)

    def __register_local(self, posted_blog_entries: list[PostedBlogEntry]):
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
            doc_entry = self.__entry_and_document_saver.save(
                posted_blog_entry.convert_to_blog_entry(), doc_content, doc_images)
            blog_content_to_doc_entry[blog_content] = doc_entry
        # 保存したものに、記事のリンクを置換してから保存し直す
        for blog_content, doc_entry in blog_content_to_doc_entry.items():
            doc_content = self.__blog_to_doc_content_converter.convert_link(blog_content, doc_entry.category_path.value)
            self.__document_file_accessor.save(doc_entry.category_path.value, doc_entry.title, doc_content)

    def __update_local(self, exist_posted_blog_entry_to_doc_entry: dict[PostedBlogEntry, DocEntry]):
        if len(exist_posted_blog_entry_to_doc_entry) == 0:
            return
        for posted_blog_entry, doc_entry in exist_posted_blog_entry_to_doc_entry.items():
            doc_entry_path = doc_entry.category_path.value
            photo_entry_to_doc_image = self.__blog_photos_to_doc_images_converter.convert_to_dict(
                posted_blog_entry.photo_entries, doc_entry_path)
            doc_content = self.__blog_to_doc_content_converter.convert(
                posted_blog_entry, doc_entry_path, photo_entry_to_doc_image)
            self.__entry_and_document_saver.save(posted_blog_entry.convert_to_blog_entry(), doc_content)
