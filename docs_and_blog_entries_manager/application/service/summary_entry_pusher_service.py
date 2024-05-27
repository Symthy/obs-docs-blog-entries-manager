from domain.blogs.datasource.interface import IBlogEntryRepository
from domain.blogs.datasource.model.not_posted_blog_entry import PrePostBlogEntry
from domain.blogs.value.blog_entry_id import BlogEntryId
from domain.entries.factory.entries_summary_factory import EntriesSummaryFactory
from domain.entries.values.category_path import CategoryPath
from infrastructure.documents.document_file_accessor import DocumentFileAccessor


class SummaryEntryPusherService:
    """
    blogとdocumentのsummary記事を更新
    """

    def __init__(self, entries_summary_factory: EntriesSummaryFactory, blog_entry_repository: IBlogEntryRepository,
                 document_file_accessor: DocumentFileAccessor, summary_entry_id: BlogEntryId):
        self.__entries_summary_factory = entries_summary_factory
        self.__blog_entry_repository = blog_entry_repository
        self.__document_file_accessor = document_file_accessor
        self.__summary_entry_id = summary_entry_id

    def execute(self):
        self.__push_doc_summary()
        self.__push_blog_summary()

    def __push_doc_summary(self):
        summary = self.__entries_summary_factory.build()
        self.__document_file_accessor.save_summary_file(summary.content)

    def __push_blog_summary(self):
        summary = self.__entries_summary_factory.build()
        summary_entry = PrePostBlogEntry(summary.title, summary.list_text, CategoryPath('Summary'), [])
        self.__blog_entry_repository.update_summary(self.__summary_entry_id, summary_entry)
