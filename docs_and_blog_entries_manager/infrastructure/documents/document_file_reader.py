from common.constants import DOCS_DIR_PATH
from domain.docs.datasources.interface import IDocumentFileReader
from domain.docs.datasources.model.document_dataset import DocumentDataset
from domain.docs.entity.doc_entries import DocEntries
from domain.docs.entity.doc_entry import DocEntry
from domain.docs.entity.factory.doc_entry_builder import DocEntryBuilder
from domain.docs.value.doc_content import DocContent
from domain.docs.value.doc_entry_id import DocEntryId
from domain.entries.values.entry_date_time import EntryDateTime
from files import file_system, text_file
from infrastructure.types import StoredDocEntriesAccessor


class DocumentFileReader(IDocumentFileReader):
    def __init__(self, stored_doc_entries_accessor: StoredDocEntriesAccessor, doc_root_dir_path: str = DOCS_DIR_PATH):
        self.__doc_root_dir_path = doc_root_dir_path
        self.__stored_doc_entries_accessor = stored_doc_entries_accessor

    def restore(self, doc_entry_file_path: str) -> DocEntry:
        doc_file_path = self.__build_file_path(doc_entry_file_path)
        content = self.load_content(doc_file_path)
        created_at = file_system.get_created_file_time(doc_file_path)
        updated_at = file_system.get_updated_file_time(doc_file_path)
        return (DocEntryBuilder()
                .id(DocEntryId(created_at))
                .title(file_system.get_file_name_without_ext(doc_file_path))
                .doc_file_name(file_system.get_file_name(doc_file_path))
                .pickup(False)
                .category_path(content.category_path)
                .categories(*content.categories)
                .created_at(EntryDateTime(created_at))
                .updated_at(EntryDateTime(updated_at))
                .build())

    def extract_entries_with_blog_category(self) -> DocEntries:
        added_blog_category_entries = []
        doc_entries = self.__stored_doc_entries_accessor.load_entries()
        for old_doc_entry in doc_entries.items_filtered_non_blog_category():
            current_doc_entry = self.restore(old_doc_entry.doc_file_path)
            current_doc_entry.contains_blog_category()
            added_blog_category_entries.append(current_doc_entry)
        return DocEntries(added_blog_category_entries)

    def find(self, doc_id: DocEntryId) -> DocumentDataset:
        doc_entry = self.__stored_doc_entries_accessor.load_entry(doc_id)
        content = self.load_content(doc_entry.doc_file_path)
        return DocumentDataset(doc_entry, content)

    def load_content(self, doc_file_path: str) -> DocContent:
        doc_file_full_path = file_system.join_path(self.__doc_root_dir_path, doc_file_path)
        content: str = text_file.read_file(doc_file_full_path)
        doc_dir_path = file_system.get_dir_path_from_file_path(doc_file_path)
        return DocContent(content, doc_dir_path)

    def __build_file_path(self, doc_entry_path: str) -> str:
        return file_system.join_path(self.__doc_root_dir_path, doc_entry_path)
