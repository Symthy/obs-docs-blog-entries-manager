import argparse

from application.service.blog_entry_pusher_service import BlogEntryPusherService
from application.service.local_doc_pusher_service import LocalDocPusherService
from cli.comand.interface import ISubCommandOption
from domain.docs.entity.doc_entry import DocEntry


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
        results = self.__local_doc_pusher_service.push_all()
        results.print_log('Successfully posted entry to local store', 'DocumentPath')
        for result in results.success_values:
            doc_entry: DocEntry = result.value
            if args.blog:
                result = self.__blog_entry_pusher_service.execute(doc_entry.id)
                result.print_log('Successfully posted entry to blog.', 'DocumentPath')
            # Todo: オプション指定が無いときは、タグによってblog投稿も行うか制御する
