import argparse

from cli.comand.interface import ISubCommand


class MainCommand:
    def __init__(self, *commands: ISubCommand):
        self.parser = argparse.ArgumentParser(description='Tool Description')
        self.subparsers = self.parser.add_subparsers(title='commands', dest='command', required=True)
        for command in commands:
            self.__init_sub_command(command)

    def __init_sub_command(self, command: ISubCommand):
        subparser = self.subparsers.add_parser(command.name(), description=command.description(), help=command.help())
        command.add_options(subparser)
        subparser.set_defaults(func=command.execute)

    def run(self):
        args = self.parser.parse_args()
        if hasattr(args, 'func'):
            args.func(args)
        else:
            self.parser.print_help()
