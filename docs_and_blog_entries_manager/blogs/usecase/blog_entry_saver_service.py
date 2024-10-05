from blogs.domain.datasource.interface import IBlogEntryModifier, StoredBlogEntriesAccessor
from blogs.domain.entity import PrePostBlogEntry
from blogs.domain.value import BlogEntryId
from blogs.exceptions.failed_save_entry_to_blog_exception import FailedSaveEntryToBlogException


class BlogEntrySaverService:
    def __init__(self, blog_entry_modifier: IBlogEntryModifier,
                 stored_blog_entries_accessor: StoredBlogEntriesAccessor):
        self.__blog_entry_modifier = blog_entry_modifier
        self.__stored_blog_entries_accessor = stored_blog_entries_accessor

    def register(self, pre_post_blog_entry: PrePostBlogEntry) -> BlogEntryId:
        blog_entry_opt = self.__blog_entry_modifier.create(pre_post_blog_entry)
        if blog_entry_opt is None:
            raise FailedSaveEntryToBlogException(pre_post_blog_entry.title, pre_post_blog_entry.category_path)
        self.__stored_blog_entries_accessor.save_entry(blog_entry_opt)
        return blog_entry_opt.id

    def update(self, pre_post_blog_entry: PrePostBlogEntry, blog_entry_id: BlogEntryId):
        old_blog_entry = self.__stored_blog_entries_accessor.load_entry(blog_entry_id)
        updated_blog_entry_opt = self.__blog_entry_modifier.update(pre_post_blog_entry, old_blog_entry)
        if updated_blog_entry_opt is None:
            raise FailedSaveEntryToBlogException(pre_post_blog_entry.title, pre_post_blog_entry.category_path)
        self.__stored_blog_entries_accessor.save_entry(updated_blog_entry_opt)
