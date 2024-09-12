import argparse

from domain.blogs.value.blog_entry_id import BlogEntryId
from infrastructure.hatena.blog_entry_repository import BlogEntryRepository

from blogs.infrastructure.hatena.api import ApiClientFactory
from cli.comand.interface import ISubCommandOption
from config.blog_config import BlogConfig


class DisplayBlogEntryOption(ISubCommandOption):
    def __init__(self, blog_config: BlogConfig):
        self.__blog_config = blog_config

    def add_option(self, subparser: argparse.ArgumentParser):
        subparser.add_argument('--display-entry', action='store', nargs=1, type=str, required=True)

    def equals(self, args):
        return args.display_entry

    def execute(self, args):
        blog_entry_id = BlogEntryId(args.display_entry[0])
        ApiClientFactory(self.__blog_config)
        api_client = ApiClientFactory(self.__blog_config).build_blog_api_client()
        repository = BlogEntryRepository(api_client, self.__blog_config.hatena_id, self.__blog_config.blog_id)
        entry_xml_data = repository.get_entry_xml_by_id(blog_entry_id)
        print(entry_xml_data)
