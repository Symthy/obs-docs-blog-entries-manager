from blogs.domain.datasource.interface import IBlogEntryFinder
from blogs.domain.entity import PostedBlogEntry
from composites.entity import BlogToDocEntryMapping
from docs.domain.entity import DocEntry
from .collected_entry_registerer import CollectedEntryRegisterer
from .collected_entry_updater import CollectedEntryUpdater


class BlogEntryCollectorService:
    """
    blogから投稿済み記事を収集し、ローカルに保存する
    """

    def __init__(self, blog_to_doc_entry_mapping: BlogToDocEntryMapping,
                 blog_entry_finder: IBlogEntryFinder,
                 collected_entry_registerer: CollectedEntryRegisterer,
                 collected_entry_updater: CollectedEntryUpdater):
        self.__blog_to_doc_mapping = blog_to_doc_entry_mapping
        self.__blog_entry_finder = blog_entry_finder
        self.__collected_entry_registerer = collected_entry_registerer
        self.__collected_entry_updater = collected_entry_updater

    def execute(self):
        all_posted_blog_entries: list[PostedBlogEntry] = self.__blog_entry_finder.find_all()
        # Todo: errorケース md保存成功して、json保存失敗したら、mdは残す（他機能で救えるため
        self.__register_all(all_posted_blog_entries)
        self.__update_all(all_posted_blog_entries)

    def __register_all(self, all_posted_blog_entries: list[PostedBlogEntry]):
        new_blog_entries = list(
            filter(lambda entry: self.__blog_to_doc_mapping.exist(entry.id), all_posted_blog_entries))
        self.__collected_entry_registerer.register(new_blog_entries)

    def __update_all(self, all_posted_blog_entries: list[PostedBlogEntry]):
        exist_blog_entry_to_doc_entry: dict[PostedBlogEntry, DocEntry] = dict(
            filter(lambda blog_entry_to_doc_entry: blog_entry_to_doc_entry[1] is not None,
                   map(lambda blog_entry: (blog_entry, self.__blog_to_doc_mapping.find_doc_entry_id(blog_entry.id)),
                       all_posted_blog_entries)))
        self.__collected_entry_updater.update(exist_blog_entry_to_doc_entry)
