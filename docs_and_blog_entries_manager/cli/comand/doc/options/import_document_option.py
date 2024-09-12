import argparse

from docs.usecase.local_doc_importer_service import LocalDocImporterService
from docs.usecase.local_doc_organizer_service import LocalDocOrganizerService
from cli.comand.interface import ISubCommandOption


class IngestDocumentOption(ISubCommandOption):
    def __init__(self, local_doc_importer_service: LocalDocImporterService,
                 local_doc_organizer_service: LocalDocOrganizerService):
        self.__local_doc_importer_service = local_doc_importer_service
        self.__local_doc_organizer_service = local_doc_organizer_service

    def add_option(self, subparser: argparse.ArgumentParser):
        subparser.add_argument('--ingest', '-i', action='store', nargs=1, type=str, required=True)

    def equals(self, args):
        return args.push

    def execute(self, args):
        self.__local_doc_importer_service.execute()
        self.__local_doc_organizer_service.organize()
