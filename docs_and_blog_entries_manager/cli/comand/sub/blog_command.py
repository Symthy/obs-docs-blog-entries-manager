import argparse

from cli.comand.interface import ISubCommand
from config.blog_config import BlogConfig
from domain.blogs.value.blog_entry_id import BlogEntryId
from infrastructure.hatena.api.api_client_factory import ApiClientFactory
from infrastructure.hatena.blog_entry_repository import BlogEntryRepository


class BlogCommand(ISubCommand):
    def __init__(self):
        self.__blog_config = BlogConfig.load()

    def name(self) -> str:
        return 'blog'

    def description(self) -> str:
        return 'operate your hatena blog.'

    def help(self) -> str:
        return 'test'

    def add_options(self, subparser: argparse.ArgumentParser):
        subparser.add_argument('--display-entry', action='store', nargs=1, type=str, required=True)

    def execute(self, args):
        if args.display_entry:
            blog_entry_id = BlogEntryId(args.display_entry[0])
            ApiClientFactory(self.__blog_config)
            api_client = ApiClientFactory(self.__blog_config).build_blog_api_client()
            repository = BlogEntryRepository(api_client, self.__blog_config.hatena_id, self.__blog_config.blog_id)
            entry_xml_data = repository.get_entry_xml_by_id(blog_entry_id)
            print(entry_xml_data)
        else:
            print('Non exist options.')
