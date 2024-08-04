from application.service.converter.Intermediate_blog_content import IntermediateBlogContent
from application.service.converter.blog_photos_to_doc_images_converter import BlogPhotosToDocImagesConverter
from application.service.converter.blog_to_doc_content_converter import BlogToDocContentConverter
from application.service.converter.blog_to_doc_entry_converter import BlogToDocEntryConverter
from domain.blogs.datasource.interface import IBlogEntryRepository
from domain.blogs.datasource.model.posted_blog_entry import PostedBlogEntry
from domain.blogs.entity.blog_entry import BlogEntry
from domain.docs.entity.doc_entry import DocEntry
from domain.docs.entity.image.doc_images import DocImages
from domain.docs.value.doc_content import DocContent
from infrastructure.documents.document_file_accessor import DocumentFileAccessor
from infrastructure.store.blog_to_doc_entry_mapping import BlogToDocEntryMapping
from infrastructure.store.composite.stored_both_entries_accessor import StoredBothEntriesAccessor


class EntryCollectorService:
    """
    blogから投稿済み記事を収集し、ローカルに保存する
    """

    def __init__(self,
                 blog_to_doc_mapping: BlogToDocEntryMapping,
                 posted_blog_entry_repository: IBlogEntryRepository,
                 blog_to_doc_entry_converter: BlogToDocEntryConverter,
                 blog_photos_to_doc_images_converter: BlogPhotosToDocImagesConverter,
                 blog_to_doc_content_converter: BlogToDocContentConverter,
                 stored_both_entries_accessor: StoredBothEntriesAccessor,
                 document_file_accessor: DocumentFileAccessor):
        self.__blog_to_doc_mapping = blog_to_doc_mapping
        self.__posted_blog_entry_repository = posted_blog_entry_repository
        self.__blog_to_doc_entry_converter = blog_to_doc_entry_converter
        self.__blog_photos_to_doc_images_converter = blog_photos_to_doc_images_converter
        self.__blog_to_doc_content_converter = blog_to_doc_content_converter
        self.__stored_both_entries_accessor = stored_both_entries_accessor

        self.__document_file_accessor = document_file_accessor

    def execute(self):
        posted_blog_entries: list[PostedBlogEntry] = self.__posted_blog_entry_repository.find_all()
        self.__save_all(posted_blog_entries)

    def __save_all(self, posted_blog_entries: list[PostedBlogEntry]):
        # Todo: errorケース md保存成功して、json保存失敗したら、mdは残す（他機能で救えるため
        new_entries = list(filter(lambda entry: self.__blog_to_doc_mapping.exist(entry.id), posted_blog_entries))
        exist_posted_blog_entry_to_doc_entry = dict(
            filter(lambda blog_entry_to_doc_entry: blog_entry_to_doc_entry[1] is not None,
                   map(lambda blog_entry: (blog_entry, self.__blog_to_doc_mapping.find_doc_entry_id(blog_entry.id)),
                       posted_blog_entries)))
        if len(new_entries) > 0:
            self.__register_documents(new_entries)
        if len(exist_posted_blog_entry_to_doc_entry) > 0:
            self.__update_documents(exist_posted_blog_entry_to_doc_entry)

    def __register_documents(self, posted_blog_entries: list[PostedBlogEntry]):
        blog_content_to_doc_entry: dict[IntermediateBlogContent, DocEntry] = {}
        # 記事のリンクを置換するためには一度全てを保存する必要があるため、リンク置換以外を行って先に保存しておく
        for posted_blog_entry in posted_blog_entries:
            blog_entry = posted_blog_entry.convert_to_blog_entry()
            doc_entry_path = posted_blog_entry.category_path.value
            photo_entry_to_doc_image = self.__blog_photos_to_doc_images_converter.convert_to_dict(
                posted_blog_entry.photo_entries, doc_entry_path)
            doc_content, blog_content = self.__blog_to_doc_content_converter.convert_for_register(
                posted_blog_entry, photo_entry_to_doc_image)
            doc_images = DocImages(list(photo_entry_to_doc_image.values()))
            doc_entry = self.__save_entry(blog_entry, doc_content, doc_images)
            blog_content_to_doc_entry[blog_content] = doc_entry
        # 保存したものに、記事のリンクを置換してから保存し直す
        for blog_content, doc_entry in blog_content_to_doc_entry.items():
            doc_content = self.__blog_to_doc_content_converter.convert_link(blog_content, doc_entry.category_path.value)
            self.__document_file_accessor.save(doc_entry.category_path.value, doc_entry.title, doc_content)

    def __update_documents(self, exist_posted_blog_entry_to_doc_entry: dict[PostedBlogEntry, DocEntry]):
        for posted_blog_entry, doc_entry in exist_posted_blog_entry_to_doc_entry.items():
            doc_entry_path = doc_entry.category_path.value
            photo_entry_to_doc_image = self.__blog_photos_to_doc_images_converter.convert_to_dict(
                posted_blog_entry.photo_entries, doc_entry_path)
            doc_content = self.__blog_to_doc_content_converter.convert(
                posted_blog_entry, doc_entry_path, photo_entry_to_doc_image)
            blog_entry = posted_blog_entry.convert_to_blog_entry()
            self.__save_entry(blog_entry, doc_content)

    def __save_entry(self, blog_entry: BlogEntry, doc_content: DocContent, doc_images: DocImages | None = None) \
            -> DocEntry:
        doc_entry_id = self.__document_file_accessor.save(
            blog_entry.category_path.value, blog_entry.title, doc_content, doc_images)
        doc_entry = self.__blog_to_doc_entry_converter.convert_to_doc_entry(blog_entry, doc_entry_id)
        self.__stored_both_entries_accessor.save_entry(blog_entry, doc_entry)
        return doc_entry
