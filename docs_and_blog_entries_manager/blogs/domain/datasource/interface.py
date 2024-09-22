from abc import ABC, abstractmethod
from typing import Optional

from blogs.domain.entity import BlogEntries
from blogs.domain.entity import BlogEntry
from blogs.domain.entity import PostedBlogEntry
from blogs.domain.entity import PrePostBlogEntry
from blogs.domain.value import BlogEntryId
from entries.domain.interface import IStoredEntriesLoader, IStoredEntriesModifier, IStoredEntriesAccessor

StoredBlogEntriesLoader = IStoredEntriesLoader[BlogEntries, BlogEntry, BlogEntryId]
StoredBlogEntriesModifier = IStoredEntriesModifier[BlogEntries, BlogEntry, BlogEntryId]
StoredBlogEntriesAccessor = IStoredEntriesAccessor[BlogEntries, BlogEntry, BlogEntryId]


class IBlogSummaryEntryUpdater(ABC):
    @abstractmethod
    def update_summary(self, entry_id: BlogEntryId, blog_summary_entry: PrePostBlogEntry) -> bool:
        pass


class IBlogEntryFinder(ABC):
    @abstractmethod
    def find(self, blog_entry_id: BlogEntryId) -> PostedBlogEntry:
        """
        :raises: FindBlogEntryException
        """
        pass

    @abstractmethod
    def find_all(self) -> list[PostedBlogEntry]:
        """
        :raises: FindAllBlogEntryException
        """
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
