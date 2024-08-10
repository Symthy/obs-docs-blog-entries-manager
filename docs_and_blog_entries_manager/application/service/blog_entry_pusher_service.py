from application.service.converter.doc_to_blog_entry_converter import DocToBlogEntryConverter
from application.service.validator.entry_link_validator import EntryLinkValidator
from common.constants import BLOG_CATEGORY
from common.result import Result
from domain.blogs.datasource.interface import IBlogEntryModifier, StoredBlogEntriesAccessor
from domain.blogs.value.blog_entry_id import BlogEntryId
from domain.docs.datasource.interface import IDocumentModifier
from domain.docs.datasource.model.document_dataset import DocumentDataset
from domain.docs.value.doc_entry_id import DocEntryId
from domain.mappings.blog_to_doc_entry_mapping import BlogToDocEntryMapping


class BlogEntryPusherService:
    """
    指定したdocumentをブログに投稿する
    """

    def __init__(self, document_file_modifier: IDocumentModifier,
                 doc_to_blog_entry_converter: DocToBlogEntryConverter,
                 blog_entry_modifier: IBlogEntryModifier,
                 blog_to_doc_mapping: BlogToDocEntryMapping,
                 stored_blog_entries_accessor: StoredBlogEntriesAccessor,
                 entry_link_validator: EntryLinkValidator):
        self.__document_file_modifier = document_file_modifier
        self.__doc_to_blog_entry_converter = doc_to_blog_entry_converter
        self.__blog_entry_modifier = blog_entry_modifier
        self.__blog_to_doc_mapping = blog_to_doc_mapping
        self.__stored_blog_entries_accessor = stored_blog_entries_accessor
        self.__entry_link_validator = entry_link_validator

    def execute(self, doc_id: DocEntryId) -> Result[str, str]:
        """
        Blogカテゴリをドキュメントに付与してブログ投稿
        """
        if not self.__entry_link_validator.validate(doc_id):
            return Result(error=f'Not posted document is linked to the blog. (id: {doc_id})')
        doc_dateset = self.__document_file_modifier.insert_category(doc_id, BLOG_CATEGORY)
        blog_entry_id_opt = self.__blog_to_doc_mapping.find_blog_entry_id(doc_id)
        if blog_entry_id_opt is None:
            return self.__post_blog(doc_dateset, doc_id)
        return self.__put_blog(doc_dateset, blog_entry_id_opt)

    def __post_blog(self, doc_dateset: DocumentDataset, doc_id: DocEntryId) -> Result[str, str]:
        pre_post_blog_entry = self.__doc_to_blog_entry_converter.convert_to_prepost(doc_dateset)
        blog_entry_opt = self.__blog_entry_modifier.create(pre_post_blog_entry)
        if blog_entry_opt is None:
            return Result(error=f'Failed to post to blog: {doc_dateset.doc_entry.doc_file_path}')
        self.__stored_blog_entries_accessor.save_entry(blog_entry_opt)
        self.__blog_to_doc_mapping.push_entry_pair(blog_entry_opt.id, doc_id)
        return Result(value=doc_dateset.doc_entry.doc_file_path)

    def __put_blog(self, doc_dateset: DocumentDataset, blog_entry_id: BlogEntryId):
        blog_entry = self.__stored_blog_entries_accessor.load_entry(blog_entry_id)
        if doc_dateset.doc_entry.updated_at <= blog_entry.updated_at:
            return Result(error=f'Skipped because blog is newer: {doc_dateset.doc_entry.doc_file_path}')
        pre_post_blog_entry = self.__doc_to_blog_entry_converter.convert_to_prepost(doc_dateset)
        blog_entry_opt = self.__blog_entry_modifier.update(pre_post_blog_entry, blog_entry)
        if blog_entry_opt is None:
            return Result(error=f'Failed to put to blog: {doc_dateset.doc_entry.doc_file_path}')
        self.__stored_blog_entries_accessor.save_entry(blog_entry_opt)
        return Result(value=doc_dateset.doc_entry.doc_file_path)
