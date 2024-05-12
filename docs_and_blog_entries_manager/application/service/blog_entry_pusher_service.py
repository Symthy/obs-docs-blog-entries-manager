from application.service.converter.doc_to_blog_entry_converter import DocToBlogEntryConverter
from application.service.store.entry_persistence_service import EntryPersistenceService
from domain.blogs.entity.blog_entry import BlogEntry
from domain.docs.datasources.model.document_dataset import DocumentDataset
from domain.docs.value.doc_entry_id import DocEntryId
from infrastructure.documents.document_file_accessor import DocumentFileAccessor
from infrastructure.hatena.blog_photo_entry_repository import BlogPhotoEntryRepository
from logs.logger import Logger


# Todo: 上書き投稿

class BlogEntryPusherService:
    def __init__(self, document_file_accessor: DocumentFileAccessor,
                 doc_to_blog_entry_converter: DocToBlogEntryConverter,
                 blog_photo_entry_repository: BlogPhotoEntryRepository,
                 entry_persistence_service: EntryPersistenceService):
        self.__document_file_accessor = document_file_accessor
        self.__doc_to_blog_entry_converter = doc_to_blog_entry_converter
        self.__blog_photo_entry_repository = blog_photo_entry_repository
        self.__entry_persistence_service = entry_persistence_service

    def execute(self, doc_id: DocEntryId):
        doc_dateset = self.__document_file_accessor.find_document(doc_id)
        blog_entry_opt = self.__push_blog(doc_dateset)
        if blog_entry_opt is None:
            Logger.error(f'Failed to push to blog: {doc_dateset.doc_entry.doc_file_path}')
        self.__entry_persistence_service.save_blog_entry(blog_entry_opt, doc_id)

    def __push_blog(self, doc_dateset: DocumentDataset) -> BlogEntry | None:
        post_blog_entry = self.__doc_to_blog_entry_converter.convert_to_post(doc_dateset)
        return self.__blog_photo_entry_repository.save(post_blog_entry)
