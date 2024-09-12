import argparse

from composites.usecase.blog_entry_all_updater_service import BlogEntryAllUpdaterService
from cli.comand.interface import ISubCommandOption


class PushBlogEntryOption(ISubCommandOption):
    """
    ローカルのドキュメントを一括でblogに反映する（新しい物は投稿し、無い物は削除する）
    """

    def __init__(self, blog_entry_all_pusher_service: BlogEntryAllUpdaterService):
        self.__blog_entry_all_pusher_service = blog_entry_all_pusher_service

    def add_option(self, subparser: argparse.ArgumentParser):
        subparser.add_argument('--push-all', action='store', nargs=1, type=str, required=True)

    def equals(self, args):
        return args.push

    def execute(self, args):
        self.__blog_entry_all_pusher_service.execute()
