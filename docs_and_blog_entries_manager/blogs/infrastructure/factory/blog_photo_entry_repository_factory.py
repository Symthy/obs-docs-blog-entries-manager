from blogs.infrastructure import BlogPhotoEntryRepository
from blogs.infrastructure.blog_entry_repository import BlogEntryRepository
from blogs.infrastructure.hatena.api import ApiClientFactory
from blogs.infrastructure.photo_entry_repository import PhotoEntryRepository
from config.blog_config import BlogConfig


class BlogPhotoEntryRepositoryFactory:
    def __init__(self, blog_conf: BlogConfig):
        self.__blog_conf = blog_conf
        self.__api_client_factory = ApiClientFactory(blog_conf)

    def build(self) -> BlogPhotoEntryRepository:
        blog_entry_repository = BlogEntryRepository(self.__api_client_factory.build_blog_api_client(),
                                                    self.__blog_conf.hatena_id, self.__blog_conf.summary_entry_id)
        photo_entry_repository = PhotoEntryRepository(self.__api_client_factory.build_photo_api_client())
        return BlogPhotoEntryRepository(blog_entry_repository, photo_entry_repository)
