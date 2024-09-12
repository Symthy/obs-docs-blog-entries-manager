import argparse

from composites.usecase.blog_entry_pusher_service import BlogEntryPusherService
from docs.usecase.local_doc_pusher_service import LocalDocPusherService
from cli.comand.interface import ISubCommandOption
from logs.logger import Logger


class PushDocumentOption(ISubCommandOption):
    def __init__(self, local_doc_pusher_service: LocalDocPusherService,
                 blog_entry_pusher_service: BlogEntryPusherService):
        self.__local_doc_pusher_service = local_doc_pusher_service
        self.__blog_entry_pusher_service = blog_entry_pusher_service

    def add_option(self, subparser: argparse.ArgumentParser):
        subparser.add_argument('--push-all', '-pa', action='store', nargs=1, type=str, required=True)
        subparser.add_argument('--blog' '-b', action='store', nargs=0, required=False)

    def equals(self, args):
        return args.push_all

    def execute(self, args):
        doc_entries = self.__local_doc_pusher_service.push_all()
        Logger.info('Successfully posted entry to local store')
        for doc_entry in doc_entries:
            if args.blog:
                self.__blog_entry_pusher_service.execute(doc_entry.id)
                Logger.info('Successfully posted entry to blog.')
            # Todo: オプション指定が無いときは、タグによってblog投稿も行うか制御する
