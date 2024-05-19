from typing import List

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
from infrastructure.store.stored_entry_accessor import _StoredEntryAccessor
from infrastructure.store.stored_entry_list_holder import StoredEntryListHolder


class DocumentFileAccessor:
    def __init__(self, document_root_dir_path, stored_entry_list: StoredEntryListHolder,
                 stored_doc_entry_accessor: _StoredEntryAccessor[DocEntry, DocEntryId]):
        self.__document_root_dir_path = document_root_dir_path
        self.__stored_entry_list = stored_entry_list
        self.__stored_doc_entry_accessor = stored_doc_entry_accessor
        self.__doc_entry_restorer = DocEntryRestorer(document_root_dir_path)

    def __load_document(self, doc_file_path: str) -> DocContent:
        content: str = text_file.read_file(file_system.join_path(doc_file_path))
        doc_dir_path = file_system.get_dir_path_from_file_path(doc_file_path)
        return DocContent(content, doc_dir_path)

    def get_file_paths(self, category_path: CategoryPath) -> List[str]:
        target_dir_path = file_system.join_path(self.__document_root_dir_path, category_path.value)
        return file_system.get_file_paths_in_target_dir(target_dir_path)

    def find_document(self, doc_id: DocEntryId) -> DocumentDataset:
        doc_entry = self.__stored_doc_entry_accessor.load_entry(doc_id)
        content = self.__load_document(doc_entry.doc_file_path)
        return DocumentDataset(doc_entry, content)

    def find_non_register_doc_entries(self, doc_entry_paths: List[str]) -> DocEntries:
        doc_id_to_path = self.__all_doc_id_to_file_path(doc_entry_paths)
        doc_entries: List[DocEntry] = []
        for doc_id, doc_entry_path in doc_id_to_path:
            if not self.__stored_entry_list.exist_id(doc_id):
                doc_entries.append(self.__doc_entry_restorer.execute(doc_entry_path))
        return DocEntries(doc_entries)

    def save_document_set(self, doc_entry_dir_path: str, title: str, content: DocContent,
                          images: DocImages) -> DocEntryId:
        doc_file_path = file_system.join_path(doc_entry_dir_path, f'{title}.md')
        text_file.write_file(doc_file_path, content.value)
        for image in images.items:
            image_file.write(image.file_path, image.image_data)
        created_date_time = EntryDateTime(file_system.get_created_file_time(doc_file_path))
        return DocEntryId(created_date_time.to_str_with_num_sequence())

    def save_summary_file(self, content: DocContent):
        summary_file_path = file_system.join_path(self.__document_root_dir_path, 'summary.md')
        text_file.write_file(summary_file_path, content.value)

    def insert_category_path_to_content(self, doc_file_path: str, category_path: CategoryPath):
        content = DocContent(text_file.read_file(doc_file_path), file_system.get_dir_path_from_file_path(doc_file_path))
        text_file.write_file(doc_file_path, content.update_category(category_path, []).value)

    def insert_category_to_content(self, doc_file_path: str, category: str):
        content = DocContent(text_file.read_file(doc_file_path), file_system.get_dir_path_from_file_path(doc_file_path))
        # Todo: refactor
        if content.not_exist_category_path:
            updated_content = content.update_category(CategoryPath(category), [])
        else:
            updated_content = content.update_category(content.category_path, [*content.categories, category])
        text_file.write_file(doc_file_path, updated_content.value)

    def __build_file_path(self, doc_file_path: str) -> str:
        return file_system.join_path(self.__document_root_dir_path, doc_file_path)

    @staticmethod
    def __all_doc_id_to_file_path(doc_entry_paths: List[str]) -> dict[DocEntryId, str]:
        doc_id_to_path: dict[DocEntryId, str] = dict(
            map(lambda path: (DocEntryId(file_system.get_created_file_time(path)), path), doc_entry_paths))
        return doc_id_to_path
