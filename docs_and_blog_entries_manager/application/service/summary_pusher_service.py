from domain.blogs.datasource.model.post_blog_entry import PostBlogEntry
from domain.blogs.value.blog_entry_id import BlogEntryId
from domain.entries.entity.category_tree_definition import CategoryTreeDefinition
from domain.entries.entity.entries_summary import EntriesSummary
from domain.entries.interface import IStoredEntriesAccessor
from domain.entries.services.entries_tree_roots_restorer import EntriesTreeRootsRestorer
from domain.entries.values.category_path import CategoryPath
from infrastructure.hatena.blog_entry_repository import BlogEntryRepository


class SummaryPusherService:
    def __init__(self, local_document_dir_path: str, summary_entry_title: str,
                 stored_entries_accessor: IStoredEntriesAccessor, blog_entry_repository: BlogEntryRepository):
        self.__local_document_dir_path = local_document_dir_path
        self.__summary_entry_title = summary_entry_title
        self.__blog_entry_repository = blog_entry_repository
        category_tree_def = CategoryTreeDefinition.build(self.__local_document_dir_path)
        self.__entries_tree_roots_restorer = EntriesTreeRootsRestorer(category_tree_def, stored_entries_accessor)

    def __build_summary(self) -> EntriesSummary:
        entries_tree_roots = self.__entries_tree_roots_restorer.execute()
        return EntriesSummary(entries_tree_roots)

    def push_doc_summary(self):
        summary = self.__build_summary()

    def push_blog_summary(self, summary_entry_id: BlogEntryId):
        summary = self.__build_summary()
        summary_entry = PostBlogEntry(self.__summary_entry_title, summary.text, CategoryPath('Summary'), [])
        self.__blog_entry_repository.put_summary_page(summary_entry_id, summary_entry)
