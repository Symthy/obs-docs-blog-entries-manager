import argparse

from application.service.blog_entry_pusher_service import BlogEntryPusherService
from cli.comand.interface import ISubCommandOption
from domain.docs.value.doc_entry_id import DocEntryId


class PushBlogEntryOption(ISubCommandOption):
    def __init__(self, blog_entry_pusher_service: BlogEntryPusherService):
        self.__blog_entry_pusher_service = blog_entry_pusher_service

    def add_option(self, subparser: argparse.ArgumentParser):
        subparser.add_argument('--push', action='store', nargs=1, type=str, required=True)

    def equals(self, args):
        return args.push

    def execute(self, args):
        doc_entry_id = DocEntryId(args.push)
        result = self.__blog_entry_pusher_service.execute(doc_entry_id)
        result.print_log()
