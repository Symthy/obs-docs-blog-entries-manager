from abc import ABC, abstractmethod

from domain.docs.datasource.model.document_dataset import DocumentDataset
from domain.docs.entity.doc_entries import DocEntries
from domain.docs.entity.doc_entry import DocEntry
from domain.docs.entity.image.doc_images import DocImages
from domain.docs.value.doc_content import DocContent
from domain.docs.value.doc_entry_id import DocEntryId
from domain.entries.interface import IStoredEntriesLoader, IStoredEntriesModifier, IStoredEntriesAccessor
from domain.entries.values.category_path import CategoryPath

StoredDocEntriesLoader = IStoredEntriesLoader[DocEntries, DocEntry, DocEntryId]
StoredDocEntriesModifier = IStoredEntriesModifier[DocEntries, DocEntry, DocEntryId]
StoredDocEntriesAccessor = IStoredEntriesAccessor[DocEntries, DocEntry, DocEntryId]


class IDocumentReader(ABC):
    @abstractmethod
    def find(self, doc_id: DocEntryId) -> DocumentDataset:
        pass

    @abstractmethod
    def restore(self, doc_entry_file_path: str) -> DocEntry:
        pass

    @abstractmethod
    def extract_entries_with_blog_category(self) -> DocEntries:
        pass

    @abstractmethod
    def extract_entries_with_non_register(self) -> DocEntries:
        pass


class IDocSummaryFileSaver(ABC):
    @abstractmethod
    def save_summary(self, content: DocContent):
        pass


class IDocumentSaver(ABC):
    @abstractmethod
    def save(self, doc_entry_dir_path: str, title: str, content: DocContent,
             images: DocImages) -> DocEntryId:
        pass


class IDocumentModifier(ABC):

    @abstractmethod
    def insert_category(self, doc_id: DocEntryId, category_to_be_added) -> DocumentDataset:
        pass

    @abstractmethod
    def insert_category_path(self, doc_file_path: str, category_path: CategoryPath) -> DocContent:
        pass

    @abstractmethod
    def delete_category(self, doc_id: DocEntryId, category_to_be_removed: str):
        pass


class IDocDocumentAccessor(IDocumentSaver, IDocSummaryFileSaver, IDocumentReader, IDocumentModifier, ABC):
    pass


class IDocumentMover(ABC):
    @abstractmethod
    def move(self, from_file_path: str, to_file_path: str):
        pass


class IWorkingDocumentReader(ABC):
    @abstractmethod
    def build_file_path(self, title: str) -> str:
        pass

    @abstractmethod
    def restore(self, title: str) -> DocEntry:
        pass

    @abstractmethod
    def extract_completed_filepaths(self) -> list[str]:
        pass
