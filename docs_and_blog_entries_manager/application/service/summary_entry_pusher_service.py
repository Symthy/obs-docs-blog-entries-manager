from domain.blogs.datasource.interface import IBlogSummaryEntryUpdater
from domain.blogs.datasource.model.pre_post_blog_entry import PrePostBlogEntry
from domain.blogs.value.blog_entry_id import BlogEntryId
from domain.docs.datasource.interface import IDocSummaryFileSaver
from domain.docs.value.doc_content import DocContent
from domain.entries.entity.entries_summary import EntriesSummary
from domain.entries.factory.entries_summary_factory import EntriesSummaryFactory
from domain.entries.values.category_path import CategoryPath


class SummaryEntryPusherService:
    """
    blogとdocumentのsummary記事を更新
    """

    def __init__(self, entries_summary_factory: EntriesSummaryFactory,
                 blog_summary_entry_updater: IBlogSummaryEntryUpdater,
                 summary_file_saver: IDocSummaryFileSaver, summary_entry_id: BlogEntryId):
        self.__entries_summary_factory = entries_summary_factory
        self.__blog_summary_entry_updater = blog_summary_entry_updater
        self.__summary_file_saver = summary_file_saver
        self.__summary_entry_id = summary_entry_id

    def execute(self):
        summary: EntriesSummary = self.__entries_summary_factory.build()
        self.__push_doc_summary(summary)
        self.__push_blog_summary(summary)

    def __push_doc_summary(self, summary: EntriesSummary):
        # サマリーはルート直下に配置
        self.__summary_file_saver.save_summary(DocContent(summary.content))

    def __push_blog_summary(self, summary: EntriesSummary):
        # CategoryPath は 実際には category として付与するのみ。実態に合わせると歪むのでこのままにする
        summary_entry = PrePostBlogEntry(summary.title, summary.text, CategoryPath(summary.category), [])
        self.__blog_summary_entry_updater.update_summary(self.__summary_entry_id, summary_entry)
