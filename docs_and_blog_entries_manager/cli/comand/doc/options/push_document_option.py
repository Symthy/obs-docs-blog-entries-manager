import argparse

from cli.comand.interface import ISubCommandOption
from composites.usecase.entry_to_blog_pusher_service import EntryToBlogPusherService
from docs.usecase.local_doc_pusher_service import LocalDocPusherService
from logs.logger import Logger


class PushDocumentOption(ISubCommandOption):
    def __init__(self, local_doc_pusher_service: LocalDocPusherService,
                 blog_entry_pusher_service: EntryToBlogPusherService):
        self.__local_doc_pusher_service = local_doc_pusher_service
        self.__blog_entry_pusher_service = blog_entry_pusher_service

    def add_option(self, subparser: argparse.ArgumentParser):
        subparser.add_argument('--push', '-p', action='store', nargs=1, type=str, required=True)
        subparser.add_argument('--blog' '-b', action='store', nargs=0, required=False)

    def equals(self, args):
        return args.push

    def execute(self, args):
        title: str = args.push
        if title is None or title == '':
            Logger.error('No specified document title.')
            return
        doc_entry = self.__local_doc_pusher_service.push(title)
        if args.blog:
            self.__blog_entry_pusher_service.execute(doc_entry.id)
