from abc import ABC, abstractmethod
from typing import Optional

from domain.blogs.datasource.model.not_posted_blog_entry import PrePostBlogEntry
from domain.blogs.datasource.model.posted_blog_entry import PostedBlogEntry
from domain.blogs.entity.blog_entry import BlogEntry
from domain.blogs.value.blog_entry_id import BlogEntryId


# Todo: 戻り値をResultに変更
class IBlogEntryRepository(ABC):

    @abstractmethod
    def find_id(self, blog_entry_id: BlogEntryId) -> PostedBlogEntry:
        pass

    @abstractmethod
    def find_all(self) -> list[PostedBlogEntry]:
        pass

    @abstractmethod
    def create(self, pre_post_blog_entry: PrePostBlogEntry) -> Optional[BlogEntry]:
        pass

    @abstractmethod
    def update(self, pre_post_blog_entry: PrePostBlogEntry, existed_blog_entry: BlogEntry) -> Optional[BlogEntry]:
        pass

    @abstractmethod
    def update_summary(self, entry_id: BlogEntryId, blog_summary_entry: PrePostBlogEntry) -> bool:
        pass

    @abstractmethod
    def delete(self, blog_entry_id: BlogEntryId) -> BlogEntry:
        pass
