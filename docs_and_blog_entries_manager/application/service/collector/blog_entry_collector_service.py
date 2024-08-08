from application.service.collector.entry_document_saver import EntryDocumentSaver
from application.service.converter.blog_photos_to_doc_images_converter import BlogPhotosToDocImagesConverter
from application.service.converter.blog_to_doc_content_converter import BlogToDocContentConverter
from domain.blogs.datasource.interface import IBlogEntryRepository
from domain.blogs.datasource.model.posted_blog_entry import PostedBlogEntry
from domain.docs.entity.doc_entry import DocEntry
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
                 entry_and_document_saver: EntryDocumentSaver):
        self.__blog_to_doc_mapping = blog_to_doc_entry_mapping
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
        new_blog_entries = list(
            filter(lambda entry: self.__blog_to_doc_mapping.exist(entry.id), posted_blog_entries))
        exist_blog_entry_to_doc_entry: dict[PostedBlogEntry, DocEntry] = dict(
            filter(lambda blog_entry_to_doc_entry: blog_entry_to_doc_entry[1] is not None,
                   map(lambda blog_entry: (blog_entry, self.__blog_to_doc_mapping.find_doc_entry_id(blog_entry.id)),
                       posted_blog_entries)))
        self.__register_local(new_blog_entries)
        self.__update_local(exist_blog_entry_to_doc_entry)
