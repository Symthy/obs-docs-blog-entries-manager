from typing import List

from common.constants import BLOG_CATEGORY
from domain.docs.datasources.interface import IDocumentRepository, IDocEntryRestorer
from domain.docs.datasources.model.document_dataset import DocumentDataset
from domain.docs.entity.doc_entries import DocEntries
from domain.docs.entity.doc_entry import DocEntry
from domain.docs.entity.image.doc_images import DocImages
from domain.docs.value.doc_content import DocContent
from domain.docs.value.doc_entry_id import DocEntryId
from domain.entries.values.category_path import CategoryPath
from domain.entries.values.entry_date_time import EntryDateTime
from files import text_file, file_system, image_file
from infrastructure.documents.doc_entry_restorer import DocEntryRestorer
from infrastructure.store.stored_entry_list_holder import StoredEntryListHolder
from infrastructure.types import StoredDocEntriesAccessor


class DocumentFileAccessor(IDocumentRepository, IDocEntryRestorer):

    def __init__(self, document_root_dir_path, stored_entry_list: StoredEntryListHolder,
                 stored_doc_entries_accessor: StoredDocEntriesAccessor):
        self.__document_root_dir_path = document_root_dir_path
        self.__stored_entry_list = stored_entry_list
        self.__stored_doc_entries_accessor = stored_doc_entries_accessor
        self.__doc_entry_restorer = DocEntryRestorer(document_root_dir_path, stored_doc_entries_accessor)

    def get_entry(self, doc_entry_file_path: str) -> DocEntry:
        return self.__doc_entry_restorer.get_entry(doc_entry_file_path)

    def extract_non_register_entries(self, doc_entry_paths: List[str]) -> DocEntries:
        doc_id_to_path = self.__all_doc_id_to_file_path(doc_entry_paths)
        doc_entries: List[DocEntry] = []
        for doc_id, doc_entry_path in doc_id_to_path:
            if not self.__stored_entry_list.exist_id(doc_id):
                doc_entries.append(self.__doc_entry_restorer.get_entry(doc_entry_path))
        return DocEntries(doc_entries)

    @classmethod
    def save(cls, doc_entry_dir_path: str, title: str, content: DocContent,
             images: DocImages) -> DocEntryId:
        doc_file_path = file_system.join_path(doc_entry_dir_path, f'{title}.md')
        text_file.write_file(doc_file_path, content.value)
        for image in images.items:
            image_file.write(image.file_path, image.image_data)
        created_date_time = EntryDateTime(file_system.get_created_file_time(doc_file_path))
        return DocEntryId(created_date_time.to_str_with_num_sequence())

    def save_summary(self, content: DocContent):
        summary_file_path = file_system.join_path(self.__document_root_dir_path, 'summary.md')
        text_file.write_file(summary_file_path, content.value)

    def insert_category(self, doc_id: DocEntryId, category_to_be_added) -> DocumentDataset:
        doc_dataset = self.__doc_entry_restorer.find(doc_id)
        new_doc_content = self.__insert_category_to_content(doc_dataset.doc_entry.doc_file_path,
                                                            doc_dataset.doc_content, category_to_be_added)
        new_doc_entry = doc_dataset.doc_entry.insert_category(category_to_be_added)
        self.__stored_doc_entries_accessor.save_entry(new_doc_entry)
        return DocumentDataset(new_doc_entry, new_doc_content)

    @classmethod
    def insert_category_path(cls, doc_file_path: str, category_path: CategoryPath) -> DocContent:
        content = DocContent(text_file.read_file(doc_file_path), file_system.get_dir_path_from_file_path(doc_file_path))
        text_file.write_file(doc_file_path, content.add_category(category_path, []).value)
        return content

    @staticmethod
    def __insert_category_to_content(doc_file_path: str, content: DocContent, category: str) -> DocContent:
        # Todo: refactor
        if BLOG_CATEGORY in content.categories:
            return content
        if content.not_exist_category_path:
            updated_content = content.add_category(CategoryPath(category), [])
        else:
            updated_content = content.add_category(content.category_path, [*content.categories, category])
        text_file.write_file(doc_file_path, updated_content.value)
        return updated_content

    def delete_category(self, doc_id: DocEntryId, category_to_be_removed: str):
        doc_dataset = self.find(doc_id)
        new_doc_entry = doc_dataset.doc_entry.remove_category(category_to_be_removed)
        new_doc_content = doc_dataset.doc_content.remove_category(category_to_be_removed)
        text_file.write_file(new_doc_entry.doc_file_path, new_doc_content.value)
        self.__stored_doc_entries_accessor.save_entry(new_doc_entry)

    def __build_file_path(self, doc_file_path: str) -> str:
        return file_system.join_path(self.__document_root_dir_path, doc_file_path)

    @staticmethod
    def __all_doc_id_to_file_path(doc_file_paths: List[str]) -> dict[DocEntryId, str]:
        doc_id_to_path: dict[DocEntryId, str] = dict(
            map(lambda path: (DocEntryId(file_system.get_created_file_time(path)), path), doc_file_paths))
        return doc_id_to_path
