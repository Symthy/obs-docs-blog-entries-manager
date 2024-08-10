from common.constants import BLOG_CATEGORY, DOCS_DIR_PATH
from domain.docs.datasource.interface import StoredDocEntriesAccessor
from domain.docs.datasource.model.document_dataset import DocumentDataset
from domain.docs.value.doc_content import DocContent
from domain.docs.value.doc_entry_id import DocEntryId
from domain.entries.values.category_path import CategoryPath
from files import text_file, file_system
from infrastructure.documents.file.document_file_finder import DocumentFileFinder


class DocumentCategoryEditor:
    def __init__(self, stored_doc_entries_accessor: StoredDocEntriesAccessor, doc_root_dir_path: str = DOCS_DIR_PATH):
        self.__stored_doc_entries_accessor = stored_doc_entries_accessor
        self.__document_file_finder = DocumentFileFinder(stored_doc_entries_accessor, doc_root_dir_path)

    def insert_category(self, doc_id: DocEntryId, category_to_be_added: str) -> DocumentDataset:
        doc_dataset = self.__document_file_finder.find(doc_id)
        new_doc_content = self.__insert_category_to_content(doc_dataset.doc_entry.doc_file_path,
                                                            doc_dataset.doc_content, category_to_be_added)
        new_doc_entry = doc_dataset.doc_entry.insert_category(category_to_be_added)
        self.__stored_doc_entries_accessor.save_entry(new_doc_entry)
        return DocumentDataset(new_doc_entry, new_doc_content)

    @staticmethod
    def __insert_category_to_content(doc_file_path: str, content: DocContent, category: str) -> DocContent:
        if category == BLOG_CATEGORY and content.contains_category(BLOG_CATEGORY):
            return content
        else:
            updated_content = content.add_category(category)
        text_file.write_file(doc_file_path, updated_content.value)
        return updated_content

    @classmethod
    def insert_category_path(cls, doc_file_path: str, category_path: CategoryPath) -> DocContent:
        content = DocContent(text_file.read_file(doc_file_path),
                             file_system.get_dir_path_from_file_path(doc_file_path))
        text_file.write_file(doc_file_path, content.update_category_path(category_path).value)
        return content

    def delete_category(self, doc_id: DocEntryId, category_to_be_removed: str):
        doc_dataset = self.__document_file_finder.find(doc_id)
        new_doc_entry = doc_dataset.doc_entry.remove_category(category_to_be_removed)
        new_doc_content = doc_dataset.doc_content.remove_category(category_to_be_removed)
        text_file.write_file(new_doc_entry.doc_file_path, new_doc_content.value)
        self.__stored_doc_entries_accessor.save_entry(new_doc_entry)
