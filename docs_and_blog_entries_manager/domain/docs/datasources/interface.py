from abc import ABC, abstractmethod

from domain.docs.datasources.model.document_dataset import DocumentDataset
from domain.docs.entity.doc_entries import DocEntries
from domain.docs.entity.image.doc_images import DocImages
from domain.docs.value.doc_content import DocContent
from domain.docs.value.doc_entry_id import DocEntryId
from domain.entries.values.category_path import CategoryPath


class IDocumentRepository(ABC):

    @abstractmethod
    def find(self, doc_id: DocEntryId) -> DocumentDataset:
        pass

    @abstractmethod
    def extract_non_register_entries(self, doc_entry_paths: list[str]) -> DocEntries:
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
