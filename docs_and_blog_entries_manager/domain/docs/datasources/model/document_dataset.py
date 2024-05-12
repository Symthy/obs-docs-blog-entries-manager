from domain.docs.entity.doc_entry import DocEntry
from domain.docs.value.doc_content import DocContent


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
