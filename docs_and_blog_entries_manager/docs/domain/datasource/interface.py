from abc import ABC, abstractmethod

from docs.domain.entity import DocumentDataset, DocEntries, DocEntry
from docs.domain.value import DocImages, DocContent, DocEntryId
from entries.domain.interface import IStoredEntriesLoader, IStoredEntriesModifier, IStoredEntriesAccessor
from entries.domain.value import CategoryPath
from files.value import FilePath, DirectoryPath

StoredDocEntriesLoader = IStoredEntriesLoader[DocEntries, DocEntry, DocEntryId]
StoredDocEntriesModifier = IStoredEntriesModifier[DocEntries, DocEntry, DocEntryId]
StoredDocEntriesAccessor = IStoredEntriesAccessor[DocEntries, DocEntry, DocEntryId]


class IDocumentReader(ABC):
    @abstractmethod
    def find(self, doc_id: DocEntryId) -> DocumentDataset:
        pass

    @abstractmethod
    def restore(self, doc_entry_file_path: FilePath) -> DocEntry:
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
    def save(self, doc_entry_dir_path: DirectoryPath, title: str, content: DocContent,
             images: DocImages | None = None) -> DocEntryId:
        pass


class IDocumentModifier(ABC):

    @abstractmethod
    def insert_category(self, doc_id: DocEntryId, category_to_be_added) -> DocumentDataset:
        pass

    @abstractmethod
    def insert_category_path_to_content(self, doc_file_path: FilePath, category_path: CategoryPath) -> DocContent:
        pass

    @abstractmethod
    def delete_category(self, doc_id: DocEntryId, category_to_be_removed: str):
        pass


class IDocumentAccessor(IDocumentSaver, IDocSummaryFileSaver, IDocumentReader, IDocumentModifier, ABC):
    pass


class IDocumentMover(ABC):
    @abstractmethod
    def move(self, from_file_path: FilePath, to_file_path: FilePath):
        pass


class IWorkingDocumentReader(ABC):
    @abstractmethod
    def build_file_path(self, title: str) -> FilePath:
        pass

    @abstractmethod
    def restore(self, title: str) -> DocEntry:
        pass

    @abstractmethod
    def extract_completed_filepaths(self) -> list[FilePath]:
        pass
