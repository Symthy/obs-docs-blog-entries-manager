import argparse
from abc import ABC, abstractmethod


class ISubCommand(ABC):
    @abstractmethod
    def name(self) -> str:
        pass

    @abstractmethod
    def description(self) -> str:
        pass

    @abstractmethod
    def help(self) -> str:
        pass

    @abstractmethod
    def add_options(self, subparser: argparse.ArgumentParser):
        """
        argparseの都合上、このようなインターフェースで妥協
        """
        pass

    @abstractmethod
    def execute(self, args):
        """コマンドの実行"""
        pass


class ISubCommandOption(ABC):
    def add_option(self, subparser: argparse.ArgumentParser):
        pass

    def equals(self, args) -> bool:
        pass

    def execute(self, args):
        pass
