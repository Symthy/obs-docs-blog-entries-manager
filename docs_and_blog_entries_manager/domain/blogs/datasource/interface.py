from abc import ABC, abstractmethod
from typing import Optional

from domain.blogs.datasource.model.posted_blog_entry import PostedBlogEntry
from domain.blogs.datasource.model.pre_post_blog_entry import PrePostBlogEntry
from domain.blogs.entity.blog_entries import BlogEntries
from domain.blogs.entity.blog_entry import BlogEntry
from domain.blogs.value.blog_entry_id import BlogEntryId
from domain.entries.interface import IStoredEntriesLoader, IStoredEntriesModifier, IStoredEntriesAccessor

StoredBlogEntriesLoader = IStoredEntriesLoader[BlogEntries, BlogEntry, BlogEntryId]
StoredBlogEntriesModifier = IStoredEntriesModifier[BlogEntries, BlogEntry, BlogEntryId]
StoredBlogEntriesAccessor = IStoredEntriesAccessor[BlogEntries, BlogEntry, BlogEntryId]


# Todo: 戻り値をResultに変更
class IBlogSummaryEntryUpdater(ABC):
    @abstractmethod
    def update_summary(self, entry_id: BlogEntryId, blog_summary_entry: PrePostBlogEntry) -> bool:
        pass


class IBlogEntryFinder(ABC):
    @abstractmethod
    def find(self, blog_entry_id: BlogEntryId) -> PostedBlogEntry:
        pass

    @abstractmethod
    def find_all(self) -> list[PostedBlogEntry]:
        pass


class IBlogEntryModifier(ABC):
    @abstractmethod
    def create(self, pre_post_blog_entry: PrePostBlogEntry) -> Optional[BlogEntry]:
        pass

    @abstractmethod
    def update(self, pre_post_blog_entry: PrePostBlogEntry, existed_blog_entry: BlogEntry) -> Optional[BlogEntry]:
        pass

    @abstractmethod
    def delete(self, blog_entry_id: BlogEntryId) -> BlogEntry:
        pass


class IBlogEntryRepository(IBlogSummaryEntryUpdater, IBlogEntryFinder, IBlogEntryModifier, ABC):
    pass
