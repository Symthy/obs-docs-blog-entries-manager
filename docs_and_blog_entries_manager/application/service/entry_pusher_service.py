from application.service.blog_entry_pusher_service import BlogEntryPusherService
from application.service.local_doc_pusher_service import LocalDocPusherService
from infrastructure.documents.work.inprogress_document_file_accessor import InprogressDocumentFileAccessor


class EntryPusherService:
    def __init__(self, blog_entry_pusher: BlogEntryPusherService, local_doc_pusher: LocalDocPusherService,
                 inprogress_doc_file_accessor: InprogressDocumentFileAccessor):
        self.__blog_entry_pusher = blog_entry_pusher
        self.__local_doc_pusher = local_doc_pusher
        self.__inprogress_doc_file_accessor = inprogress_doc_file_accessor

    def execute(self):
        completed_work_filepaths = self.__inprogress_doc_file_accessor.extract_completed_filepaths()
        for file_path in completed_work_filepaths:
            doc_id = self.__local_doc_pusher.push(file_path)
            self.__blog_entry_pusher.execute(doc_id)
