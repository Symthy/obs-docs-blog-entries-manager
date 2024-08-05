import argparse

from application.service.blog_entry_collector_service import BlogEntryCollectorService
from cli.comand.interface import ISubCommandOption


class CollectBlogEntryOption(ISubCommandOption):
    def __init__(self, entry_collector_service: BlogEntryCollectorService):
        self.__entry_collector_service = entry_collector_service

    def add_option(self, subparser: argparse.ArgumentParser):
        subparser.add_argument('--collect', action='store', nargs=0, required=False)

    def equals(self, args):
        return args.collect

    def execute(self, _):
        self.__entry_collector_service.execute()
