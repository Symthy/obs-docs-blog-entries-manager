from application.service.blog_entry_pusher_service import BlogEntryPusherService
from application.service.local_doc_pusher_service import LocalDocPusherService
from infrastructure.documents.work.working_document_file_accessor import WorkingDocumentFileAccessor


class EntryPusherService:
    """
    workフォルダの完成記事をdocumentフォルダに格納し、blogにも投稿
    """

    def __init__(self, blog_entry_pusher: BlogEntryPusherService, local_doc_pusher: LocalDocPusherService,
                 working_doc_file_accessor: WorkingDocumentFileAccessor):
        self.__blog_entry_pusher = blog_entry_pusher
        self.__local_doc_pusher = local_doc_pusher
        self.__working_doc_file_accessor = working_doc_file_accessor

    def execute(self):
        completed_work_filepaths = self.__working_doc_file_accessor.extract_completed_filepaths()
        for file_path in completed_work_filepaths:
            doc_entry = self.__local_doc_pusher.execute(file_path)
            if doc_entry.contains_blog_category():
                self.__blog_entry_pusher.execute(doc_entry.id)
