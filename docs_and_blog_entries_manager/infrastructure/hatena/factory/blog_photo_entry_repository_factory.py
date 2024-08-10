from config.blog_config import BlogConfig
from domain.blogs.value.blog_entry_id import BlogEntryId
from infrastructure.hatena.api.api_client_factory import ApiClientFactory
from infrastructure.hatena.blog_entry_repository import BlogEntryRepository
from infrastructure.hatena.blog_photo_entry_repository import BlogPhotoEntryRepository
from infrastructure.hatena.photo_entry_repository import PhotoEntryRepository


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
