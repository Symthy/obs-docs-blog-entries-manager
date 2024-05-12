from domain.blogs.datasource.model.post_blog_entry import PostBlogEntry
from domain.blogs.entity.blog_entry import BlogEntry
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
        posted_blog_entry_opt.merge_photo_entries(photo_entries)
        return posted_blog_entry_opt.convert_to_blog_entry()
