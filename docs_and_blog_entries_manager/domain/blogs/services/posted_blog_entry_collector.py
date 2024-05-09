from typing import List

from domain.blogs.datasource.model.posted_blog_entry import PostedBlogEntry
from domain.blogs.entity.photo.photo_entries import PhotoEntries
from domain.blogs.entity.photo.photo_entry import PhotoEntry
from domain.blogs.value.photo_entry_id import PhotoEntryId
from infrastructure.hatena.blog_entry_repository import BlogEntryRepository
from infrastructure.hatena.photo_entry_repository import PhotoEntryRepository


class PostedBlogEntryCollector:
    def __init__(self, hatena_id: str, blog_entry_repository: BlogEntryRepository,
                 photo_entry_repository: PhotoEntryRepository):
        self.__hatena_id = hatena_id
        self.__blog_entry_repository = blog_entry_repository
        self.__photo_entry_repository = photo_entry_repository

    def execute(self) -> List[PostedBlogEntry]:
        posted_blog_entries: List[PostedBlogEntry] = []
        for posted_blog_entry in self.__blog_entry_repository.all():
            photo_entry_ids: List[PhotoEntryId] = posted_blog_entry.content.photo_entry_ids
            updated_posted_blog_entry = self.__insert_photo_entries(posted_blog_entry, photo_entry_ids)
            posted_blog_entries.append(updated_posted_blog_entry)
        return posted_blog_entries

    def __insert_photo_entries(self, posted_blog_entry: PostedBlogEntry,
                               photo_entry_ids: List[PhotoEntryId]) -> PostedBlogEntry:
        photo_entries: List[PhotoEntry] = []
        for photo_entry_id in photo_entry_ids:
            photo_entry = self.__photo_entry_repository.find_id(photo_entry_id)
            if photo_entry is not None:
                photo_entries.append(photo_entry)
        new_posted_blog_entry = posted_blog_entry.merge_photo_entries(PhotoEntries(photo_entries))
        return new_posted_blog_entry
