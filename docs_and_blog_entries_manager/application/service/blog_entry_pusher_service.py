from application.service.converter.doc_to_blog_entry_converter import DocToBlogEntryConverter
from common.constants import BLOG_CATEGORY
from common.result import Result
from domain.blogs.datasource.interface import IBlogEntryRepository
from domain.blogs.entity.blog_entry import BlogEntry
from domain.docs.datasources.model.document_dataset import DocumentDataset
from domain.docs.value.doc_entry_id import DocEntryId
from infrastructure.documents.document_file_accessor import DocumentFileAccessor
from infrastructure.store.blog_to_doc_entry_mapping import BlogToDocEntryMapping
from infrastructure.types import StoredBlogEntriesAccessor


class BlogEntryPusherService:
    """
    指定したdocumentをブログに投稿する
    """

    def __init__(self, document_file_accessor: DocumentFileAccessor,
                 doc_to_blog_entry_converter: DocToBlogEntryConverter,
                 blog_photo_entry_repository: IBlogEntryRepository,
                 blog_to_doc_mapping: BlogToDocEntryMapping,
                 stored_blog_entries_accessor: StoredBlogEntriesAccessor):
        self.__document_file_accessor = document_file_accessor
        self.__doc_to_blog_entry_converter = doc_to_blog_entry_converter
        self.__blog_photo_entry_repository = blog_photo_entry_repository
        self.__blog_to_doc_mapping = blog_to_doc_mapping
        self.__stored_blog_entries_accessor = stored_blog_entries_accessor

    def execute(self, doc_id: DocEntryId) -> Result[str, str]:
        """
        Blogカテゴリをドキュメントに付与してブログ投稿
        """
        doc_dateset = self.__document_file_accessor.insert_category(doc_id, BLOG_CATEGORY)
        blog_entry_id_opt = self.__blog_to_doc_mapping.find_blog_entry_id(doc_id)
        if blog_entry_id_opt is None:
            return self.__post_blog(doc_dateset, doc_id)
        blog_entry = self.__stored_blog_entries_accessor.load_entry(blog_entry_id_opt)
        if doc_dateset.doc_entry.updated_at > blog_entry.updated_at:
            return self.__put_blog(doc_dateset, blog_entry)

    def __post_blog(self, doc_dateset: DocumentDataset, doc_id: DocEntryId) -> Result[str, str]:
        pre_post_blog_entry = self.__doc_to_blog_entry_converter.convert_to_prepost(doc_dateset)
        blog_entry_opt = self.__blog_photo_entry_repository.create(pre_post_blog_entry)
        if blog_entry_opt is None:
            return Result(error=f'Failed to post to blog: {doc_dateset.doc_entry.doc_file_path}')
        self.__stored_blog_entries_accessor.save_entry(blog_entry_opt)
        self.__blog_to_doc_mapping.push_entry_pair(blog_entry_opt.id, doc_id)
        return Result(value=doc_dateset.doc_entry.doc_file_path)

    def __put_blog(self, doc_dateset: DocumentDataset, blog_entry: BlogEntry):
        pre_post_blog_entry = self.__doc_to_blog_entry_converter.convert_to_prepost(doc_dateset)
        blog_entry_opt = self.__blog_photo_entry_repository.update(pre_post_blog_entry, blog_entry)
        if blog_entry_opt is None:
            return Result(error=f'Failed to put to blog: {doc_dateset.doc_entry.doc_file_path}')
        self.__stored_blog_entries_accessor.save_entry(blog_entry_opt)
        return Result(value=doc_dateset.doc_entry.doc_file_path)
