from docs.domain.value import DocContent
from .doc_entry import DocEntry


class DocumentDataset:
    def __init__(self, doc_entry: DocEntry, doc_content: DocContent):
        self.__doc_entry = doc_entry
        self.__doc_content = doc_content

    @property
    def doc_entry(self) -> DocEntry:
        return self.__doc_entry

    @property
    def doc_content(self) -> DocContent:
        return self.__doc_content
