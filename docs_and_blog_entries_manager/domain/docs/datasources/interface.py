from abc import ABC, abstractmethod

from domain.docs.datasources.model.document_dataset import DocumentDataset
from domain.docs.entity.doc_entries import DocEntries
from domain.docs.entity.doc_entry import DocEntry
from domain.docs.entity.image.doc_images import DocImages
from domain.docs.value.doc_content import DocContent
from domain.docs.value.doc_entry_id import DocEntryId
from domain.entries.values.category_path import CategoryPath


class IDocumentAccessor(ABC):

    @abstractmethod
    def extract_entries_with_non_register(self, doc_entry_paths: list[str]) -> DocEntries:
        pass

    @abstractmethod
    def save(self, doc_entry_dir_path: str, title: str, content: DocContent,
             images: DocImages) -> DocEntryId:
        pass

    @abstractmethod
    def save_summary(self, content: DocContent):
        pass

    @abstractmethod
    def insert_category(self, doc_id: DocEntryId, category_to_be_added) -> DocumentDataset:
        pass

    @abstractmethod
    def insert_category_path(cls, doc_file_path: str, category_path: CategoryPath) -> DocContent:
        pass

    @abstractmethod
    def delete_category(self, doc_id: DocEntryId, category_to_be_removed: str):
        pass


class IDocumentFileReader(ABC):
    @abstractmethod
    def restore(self, doc_entry_file_path: str) -> DocEntry:
        pass

    @abstractmethod
    def extract_entries_with_blog_category(self) -> DocEntries:
        pass


class IDocumentMover(ABC):
    @abstractmethod
    def move(self, from_file_path: str, doc_entry: DocEntry):
        pass
