from typing import Optional

from domain.blogs.datasource.interface import IBlogEntryRepository
from domain.blogs.datasource.model.posted_blog_entry import PostedBlogEntry
from domain.blogs.datasource.model.pre_post_blog_entry import PrePostBlogEntry
from domain.blogs.entity.blog_entry import BlogEntry
from domain.blogs.entity.photo.photo_entries import PhotoEntries
from domain.blogs.entity.photo.photo_entry import PhotoEntry
from domain.blogs.value.blog_entry_id import BlogEntryId
from domain.blogs.value.photo_entry_id import PhotoEntryId
from files import file_system
from infrastructure.hatena.blog_entry_repository import BlogEntryRepository
from infrastructure.hatena.photo_entry_repository import PhotoEntryRepository


class BlogPhotoEntryRepository(IBlogEntryRepository):
    def __init__(self, blog_entry_repository: BlogEntryRepository,
                 photo_entry_repository: PhotoEntryRepository):
        self.__blog_entry_repository = blog_entry_repository
        self.__photo_entry_repository = photo_entry_repository

    def find(self, blog_entry_id: BlogEntryId) -> PostedBlogEntry:
        posted_blog_entry = self.__blog_entry_repository.find(blog_entry_id)
        photo_entry_ids: list[PhotoEntryId] = posted_blog_entry.content.photo_entry_ids
        posted_blog_entry_has_photo = self.__insert_photo_entries(posted_blog_entry, photo_entry_ids)
        return posted_blog_entry_has_photo

    def find_all(self) -> list[PostedBlogEntry]:
        posted_blog_entries: list[PostedBlogEntry] = []
        for posted_blog_entry in self.__blog_entry_repository.find_all():
            photo_entry_ids: list[PhotoEntryId] = posted_blog_entry.content.photo_entry_ids
            posted_blog_entry_has_photo = self.__insert_photo_entries(posted_blog_entry, photo_entry_ids)
            posted_blog_entries.append(posted_blog_entry_has_photo)
        return posted_blog_entries

    def __insert_photo_entries(self, posted_blog_entry: PostedBlogEntry,
                               photo_entry_ids: list[PhotoEntryId]) -> PostedBlogEntry:
        photo_entries: list[PhotoEntry] = []
        for photo_entry_id in photo_entry_ids:
            photo_entry = self.__photo_entry_repository.find_id(photo_entry_id)
            if photo_entry is not None:
                photo_entries.append(photo_entry)
        new_posted_blog_entry = posted_blog_entry.merge_photo_entries(PhotoEntries(photo_entries))
        return new_posted_blog_entry

    def create(self, pre_post_blog_entry: PrePostBlogEntry) -> Optional[BlogEntry]:
        posted_blog_entry_opt = self.__blog_entry_repository.create(pre_post_blog_entry)
        if posted_blog_entry_opt is None:
            return None
        photo_entries = self.__photo_entry_repository.create_all(pre_post_blog_entry.doc_image_paths)
        # Todo: 後からマージするのは微妙
        posted_blog_entry_opt.merge_photo_entries(photo_entries)
        return posted_blog_entry_opt.convert_to_blog_entry()

    def update(self, pre_post_blog_entry: PrePostBlogEntry, existed_blog_entry: BlogEntry) -> Optional[BlogEntry]:
        posted_blog_entry_opt = self.__blog_entry_repository.update(existed_blog_entry.id, pre_post_blog_entry)
        if posted_blog_entry_opt is None:
            return None
        for image_path in pre_post_blog_entry.doc_image_paths:
            image_filename = file_system.get_file_name_from_file_path(image_path)
            photo_entry_opt = existed_blog_entry.images.get_entry(image_filename)
            if photo_entry_opt is None:
                self.__photo_entry_repository.create(image_path)
            else:
                self.__photo_entry_repository.update(image_filename, photo_entry_opt)
        photo_entries_to_be_deleted = existed_blog_entry.images.non_exist_entries(
            pre_post_blog_entry.doc_image_filenames)
        self.__photo_entry_repository.delete_all(photo_entries_to_be_deleted)

    def update_summary(self, entry_id: BlogEntryId, blog_summary_entry: PrePostBlogEntry) -> bool:
        self.__blog_entry_repository.update_summary(entry_id, blog_summary_entry)

    def delete(self, blog_entry_id: BlogEntryId) -> BlogEntry:
        # Todo
        pass
