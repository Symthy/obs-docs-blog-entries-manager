from blogs.domain.value import BlogEntryId
from blogs.infrastructure import BlogEntryRepository, BlogPhotoEntryRepository, PhotoEntryRepository
from blogs.infrastructure.hatena.api import ApiClientFactory
from config.blog_config import BlogConfig


class BlogPhotoEntryRepositoryFactory:
    def __init__(self, blog_conf: BlogConfig, summary_entry_id: BlogEntryId):
        self.__blog_conf = blog_conf
        self.__api_client_factory = ApiClientFactory(blog_conf)
        self.__summary_entry_id = summary_entry_id

    def build(self) -> BlogPhotoEntryRepository:
        blog_entry_repository = BlogEntryRepository(self.__api_client_factory.build_blog_api_client(),
                                                    self.__blog_conf.hatena_id, self.__summary_entry_id)
        photo_entry_repository = PhotoEntryRepository(self.__api_client_factory.build_photo_api_client())
        return BlogPhotoEntryRepository(blog_entry_repository, photo_entry_repository)
