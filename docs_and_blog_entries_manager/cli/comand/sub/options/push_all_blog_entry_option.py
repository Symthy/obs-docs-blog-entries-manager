import argparse

from application.service.blog_entry_all_pusher_service import BlogEntryAllPusherService
from cli.comand.interface import ISubCommandOption


class PushBlogEntryOption(ISubCommandOption):
    def __init__(self, blog_entry_all_pusher_service: BlogEntryAllPusherService):
        self.__blog_entry_all_pusher_service = blog_entry_all_pusher_service

    def add_option(self, subparser: argparse.ArgumentParser):
        subparser.add_argument('--push-all', action='store', nargs=1, type=str, required=True)

    def equals(self, args):
        return args.push

    def execute(self, args):
        result = self.__blog_entry_all_pusher_service.execute()
        result.print_log()
