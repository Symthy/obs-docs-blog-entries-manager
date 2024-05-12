from domain.blogs.datasource.model.post_blog_entry import PostBlogEntry
from domain.blogs.entity.blog_entry import BlogEntry
from files import file_system
from infrastructure.hatena.blog_entry_repository import BlogEntryRepository
from infrastructure.hatena.photo_entry_repository import PhotoEntryRepository


class BlogPhotoEntryRepository:
    def __init__(self, blog_entry_repository: BlogEntryRepository, photo_entry_repository: PhotoEntryRepository):
        self.__blog_entry_repository = blog_entry_repository
        self.__photo_entry_repository = photo_entry_repository

    def save(self, post_blog_entry: PostBlogEntry) -> BlogEntry | None:
        posted_blog_entry_opt = self.__blog_entry_repository.post(post_blog_entry)
        if posted_blog_entry_opt is None:
            return None
        photo_entries = self.__photo_entry_repository.post_all(post_blog_entry.doc_image_paths)
        # Todo: 後からマージするのは微妙
        posted_blog_entry_opt.merge_photo_entries(photo_entries)
        return posted_blog_entry_opt.convert_to_blog_entry()

    def update(self, post_blog_entry: PostBlogEntry, existed_blog_entry: BlogEntry) -> BlogEntry | None:
        posted_blog_entry_opt = self.__blog_entry_repository.put(post_blog_entry)
        if posted_blog_entry_opt is None:
            return None
        for image_path in post_blog_entry.doc_image_paths:
            image_filename = file_system.get_file_name_from_file_path(image_path)
            photo_entry_opt = existed_blog_entry.images.get_entry(image_filename)
            if photo_entry_opt is None:
                self.__photo_entry_repository.post(image_path)
            else:
                self.__photo_entry_repository.put(image_filename, photo_entry_opt)
        photo_entries_to_be_deleted = existed_blog_entry.images.non_exist_entries(post_blog_entry.doc_image_filenames)
        self.__photo_entry_repository.delete_all(photo_entries_to_be_deleted)
