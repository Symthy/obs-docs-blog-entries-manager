import argparse

from cli.comand.interface import ISubCommand, ISubCommandOption


class BlogCommand(ISubCommand):
    def __init__(self, blog_config, *options: ISubCommandOption):
        self.__blog_config = blog_config
        self.__options = options

    def name(self) -> str:
        return 'blog'

    def description(self) -> str:
        return 'operate your hatena blog.'

    def help(self) -> str:
        return 'test'

    def add_options(self, subparser: argparse.ArgumentParser):
        subparser.add_argument('--display-entry', action='store', nargs=1, type=str, required=True)

    def execute(self, args):
        for option in self.__options:
            if option.equals(args):
                option.execute(args)
                return
        print('Non exist options.')
