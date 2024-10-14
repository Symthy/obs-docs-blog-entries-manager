from typing import Optional

from blogs.domain.datasource.interface import IBlogEntryRepository
from blogs.domain.entity import BlogEntry, PhotoEntry, PhotoEntries, PostedBlogEntry, PrePostBlogEntry
from blogs.domain.value import BlogEntryId, PhotoEntryId
from .blog_repository import BlogRepository
from .photo_entry_repository import PhotoEntryRepository


class BlogEntryRepository(IBlogEntryRepository):
    def __init__(self, blog_entry_repository: BlogRepository,
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
        # 後からマージするのは微妙だが、良い方法思いつかないのでこうしておく
        posted_blog_entry = posted_blog_entry_opt.merge_photo_entries(photo_entries)
        return posted_blog_entry.blog_entry()

    def update(self, pre_post_blog_entry: PrePostBlogEntry, old_blog_entry: BlogEntry) -> Optional[BlogEntry]:
        posted_blog_entry_opt = self.__blog_entry_repository.update(old_blog_entry.id, pre_post_blog_entry)
        if posted_blog_entry_opt is None:
            return None
        for image_path in pre_post_blog_entry.doc_image_paths:
            image_filename = image_path.get_file_name()
            photo_entry_opt = old_blog_entry.images.get_entry(image_filename)
            if photo_entry_opt is None:
                self.__photo_entry_repository.create(image_path)
            else:
                self.__photo_entry_repository.update(image_path, photo_entry_opt)
        photo_entries_to_be_deleted = old_blog_entry.images.non_exist_entries(
            pre_post_blog_entry.doc_image_filenames)
        self.__photo_entry_repository.delete_all(photo_entries_to_be_deleted)

    def update_summary(self, entry_id: BlogEntryId, blog_summary_entry: PrePostBlogEntry):
        self.__blog_entry_repository.update_summary(entry_id, blog_summary_entry)

    def delete(self, blog_entry_id: BlogEntryId) -> BlogEntry:
        # Todo
        pass
