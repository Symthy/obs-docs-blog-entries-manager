from blogs.domain.datasource.interface import StoredBlogEntriesAccessor
from blogs.domain.value import BlogEntryId
from blogs.usecase import BlogEntrySaverService
from common.constants import BLOG_CATEGORY
from composites.converter import DocToBlogEntryConverter
from composites.entity import BlogToDocEntryMapping
from composites.exceptions.document_linked_entry_illegal_exception import DocumentLinkedEntryIllegalException
from docs.domain.datasource.interface import IDocumentModifier
from docs.domain.entity import DocumentDataset
from docs.domain.value import DocEntryId
from docs.usecase.validator import DocEntryLinkValidator
from logs.logger import Logger


class EntryToBlogPusherService:
    """
    指定したdocumentをブログに投稿する
    """

    def __init__(self, document_file_modifier: IDocumentModifier,
                 doc_to_blog_entry_converter: DocToBlogEntryConverter,
                 blog_to_doc_mapping: BlogToDocEntryMapping,
                 entry_link_validator: DocEntryLinkValidator,
                 blog_entry_saver: BlogEntrySaverService,
                 stored_blog_entries_accessor: StoredBlogEntriesAccessor):
        self.__document_file_modifier = document_file_modifier
        self.__doc_to_blog_entry_converter = doc_to_blog_entry_converter
        self.__blog_to_doc_mapping = blog_to_doc_mapping
        self.__entry_link_validator = entry_link_validator
        self.__stored_blog_entries_accessor = stored_blog_entries_accessor
        self.__blog_entry_saver = blog_entry_saver

    def execute(self, doc_id: DocEntryId):
        """
        Blogカテゴリをドキュメントに付与してブログ投稿
        """
        if not self.__entry_link_validator.validate(doc_id):
            raise DocumentLinkedEntryIllegalException(doc_id)
        doc_dateset = self.__document_file_modifier.insert_category(doc_id, BLOG_CATEGORY)
        blog_entry_id_opt = self.__blog_to_doc_mapping.find_blog_entry_id(doc_id)
        if blog_entry_id_opt is None:
            self.__register_to_blog(doc_dateset, doc_id)
        else:
            self.__update_to_blog(doc_dateset, blog_entry_id_opt)

    def __register_to_blog(self, doc_dateset: DocumentDataset, doc_id: DocEntryId):
        pre_post_blog_entry = self.__doc_to_blog_entry_converter.convert_to_prepost(doc_dateset)
        blog_entry_id = self.__blog_entry_saver.register(pre_post_blog_entry)
        self.__blog_to_doc_mapping.push_entry_pair(blog_entry_id, doc_id)

    def __update_to_blog(self, doc_dateset: DocumentDataset, blog_entry_id: BlogEntryId):
        blog_entry = self.__stored_blog_entries_accessor.load_entry(blog_entry_id)
        if doc_dateset.doc_entry.updated_at <= blog_entry.updated_at:
            Logger.info(f'Skipped because blog is newer: {doc_dateset.doc_entry.doc_file_path}')
            return
        pre_post_blog_entry = self.__doc_to_blog_entry_converter.convert_to_prepost(doc_dateset)
        self.__blog_entry_saver.update(pre_post_blog_entry, blog_entry_id)
