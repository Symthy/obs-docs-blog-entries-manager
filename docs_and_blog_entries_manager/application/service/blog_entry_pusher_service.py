from application.service.converter.doc_to_blog_entry_converter import DocToBlogEntryConverter
from application.service.store.entry_persistence_service import EntryPersistenceService
from domain.blogs.entity.blog_entry import BlogEntry
from domain.blogs.value.blog_entry_id import BlogEntryId
from domain.docs.datasources.model.document_dataset import DocumentDataset
from domain.docs.value.doc_entry_id import DocEntryId
from infrastructure.documents.document_file_accessor import DocumentFileAccessor
from infrastructure.hatena.blog_photo_entry_repository import BlogPhotoEntryRepository
from infrastructure.store.blog_to_doc_entry_mapping import BlogToDocEntryMapping
from infrastructure.store.stored_entry_accessor import StoredEntryAccessor
from logs.logger import Logger


# Todo: refactor 依存関係減らせないか

class BlogEntryPusherService:
    def __init__(self, document_file_accessor: DocumentFileAccessor,
                 doc_to_blog_entry_converter: DocToBlogEntryConverter,
                 blog_photo_entry_repository: BlogPhotoEntryRepository,
                 blog_to_doc_mapping: BlogToDocEntryMapping,
                 stored_blog_entry_accessor: StoredEntryAccessor[BlogEntry, BlogEntryId],
                 entry_persistence_service: EntryPersistenceService):
        self.__document_file_accessor = document_file_accessor
        self.__doc_to_blog_entry_converter = doc_to_blog_entry_converter
        self.__blog_photo_entry_repository = blog_photo_entry_repository
        self.__blog_to_doc_mapping = blog_to_doc_mapping
        self.__stored_blog_entry_accessor = stored_blog_entry_accessor
        self.__entry_persistence_service = entry_persistence_service

    def execute(self, doc_id: DocEntryId):
        doc_dateset = self.__document_file_accessor.find_document(doc_id)
        blog_entry_id_opt = self.__blog_to_doc_mapping.find_blog_entry_id(doc_id)
        if blog_entry_id_opt is None:
            self.__post_blog(doc_dateset, doc_id)
        blog_entry = self.__stored_blog_entry_accessor.load_entry(blog_entry_id_opt)
        if doc_dateset.doc_entry.updated_at > blog_entry.updated_at:
            self.__put_blog(doc_dateset, blog_entry)

    def __post_blog(self, doc_dateset: DocumentDataset, doc_id: DocEntryId):
        post_blog_entry = self.__doc_to_blog_entry_converter.convert_to_post(doc_dateset)
        blog_entry_opt = self.__blog_photo_entry_repository.save(post_blog_entry)
        if blog_entry_opt is None:
            Logger.error(f'Failed to push to blog: {doc_dateset.doc_entry.doc_file_path}')
            return
        self.__entry_persistence_service.save_blog_entry(blog_entry_opt, doc_id)

    def __put_blog(self, doc_dateset: DocumentDataset, blog_entry: BlogEntry):
        post_blog_entry = self.__doc_to_blog_entry_converter.convert_to_post(doc_dateset)
        blog_entry_opt = self.__blog_photo_entry_repository.update(post_blog_entry, blog_entry)
        if blog_entry_opt is None:
            Logger.error(f'Failed to put to blog: {doc_dateset.doc_entry.doc_file_path}')
            return
        self.__stored_blog_entry_accessor.save_entry(blog_entry_opt)
