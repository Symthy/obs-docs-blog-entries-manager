import argparse

from application.service.blog_entry_pusher_service import BlogEntryPusherService
from application.service.local_doc_pusher_service import LocalDocPusherService
from cli.comand.interface import ISubCommandOption
from logs.logger import Logger


class PushDocumentOption(ISubCommandOption):
    def __init__(self, local_doc_pusher_service: LocalDocPusherService,
                 blog_entry_pusher_service: BlogEntryPusherService):
        self.__local_doc_pusher_service = local_doc_pusher_service
        self.__blog_entry_pusher_service = blog_entry_pusher_service

    def add_option(self, subparser: argparse.ArgumentParser):
        subparser.add_argument('--push', action='store', nargs=1, type=str, required=True)
        subparser.add_argument('--blog', action='store', nargs=0, required=False)

    def equals(self, args):
        return args.push

    def execute(self, args):
        title: str = args.push
        if title is None or title == '':
            Logger.error('No specified document title.')
            return
        result = self.__local_doc_pusher_service.execute(title)
        if result.failure:
            result.print_error()
            return
        result = self.__blog_entry_pusher_service.execute(result.value)
        result.print_log('Successfully posted document to blog.', 'DocumentPath:')
