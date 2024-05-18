from domain.blogs.datasource.model.post_blog_entry import PostBlogEntry
from domain.blogs.value.blog_entry_id import BlogEntryId
from domain.entries.factory.entries_summary_factory import EntriesSummaryFactory
from domain.entries.values.category_path import CategoryPath
from infrastructure.documents.document_file_accessor import DocumentFileAccessor
from infrastructure.hatena.blog_entry_repository import BlogEntryRepository


class SummaryPusherService:
    def __init__(self, entries_summary_factory: EntriesSummaryFactory, blog_entry_repository: BlogEntryRepository,
                 document_file_accessor: DocumentFileAccessor):
        self.__entries_summary_factory = entries_summary_factory
        self.__blog_entry_repository = blog_entry_repository
        self.__document_file_accessor = document_file_accessor

    def push_doc_summary(self):
        summary = self.__entries_summary_factory.build()
        self.__document_file_accessor.save_summary_file(summary.content)

    def push_blog_summary(self, summary_entry_id: BlogEntryId):
        summary = self.__entries_summary_factory.build()
        summary_entry = PostBlogEntry(summary.title, summary.list_text, CategoryPath('Summary'), [])
        self.__blog_entry_repository.put_summary_page(summary_entry_id, summary_entry)