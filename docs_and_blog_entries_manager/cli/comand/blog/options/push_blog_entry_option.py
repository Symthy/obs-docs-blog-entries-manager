import argparse

from cli.comand.interface import ISubCommandOption
from composites.usecase.entry_to_blog_pusher_service import EntryToBlogPusherService
from docs.domain.value import DocEntryId


class PushBlogEntryOption(ISubCommandOption):
    def __init__(self, blog_entry_pusher_service: EntryToBlogPusherService):
        self.__blog_entry_pusher_service = blog_entry_pusher_service

    def add_option(self, subparser: argparse.ArgumentParser):
        subparser.add_argument('--push', action='store', nargs=1, type=str, required=True)

    def equals(self, args):
        return args.push

    def execute(self, args):
        doc_entry_id = DocEntryId(args.push)
        self.__blog_entry_pusher_service.execute(doc_entry_id)
