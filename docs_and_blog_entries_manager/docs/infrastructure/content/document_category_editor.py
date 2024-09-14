from common.constants import BLOG_CATEGORY, DOCS_DIR_PATH
from docs.domain.datasource.interface import StoredDocEntriesAccessor
from docs.domain.entity import DocumentDataset
from docs.domain.value import DocContent, DocEntryId
from docs.infrastructure.file.document_file_finder import DocumentFileFinder
from entries.domain.value import CategoryPath
from files import text_file
from files.value import FilePath, DirectoryPath


class DocumentCategoryEditor:
    def __init__(self, stored_doc_entries_accessor: StoredDocEntriesAccessor,
                 doc_root_dir_path: DirectoryPath = DOCS_DIR_PATH):
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
    def __insert_category_to_content(doc_file_path: FilePath, content: DocContent, category: str) -> DocContent:
        if category == BLOG_CATEGORY and content.contains_category(BLOG_CATEGORY):
            return content
        else:
            updated_content = content.add_category(category)
        text_file.write_file(doc_file_path, updated_content.value)
        return updated_content

    @classmethod
    def insert_category_path(cls, doc_file_path: FilePath, category_path: CategoryPath) -> DocContent:
        content = DocContent(text_file.read_file(doc_file_path))
        text_file.write_file(doc_file_path, content.update_category_path(category_path).value)
        return content

    def delete_category(self, doc_id: DocEntryId, category_to_be_removed: str):
        doc_dataset = self.__document_file_finder.find(doc_id)
        new_doc_entry = doc_dataset.doc_entry.remove_category(category_to_be_removed)
        new_doc_content = doc_dataset.doc_content.remove_category(category_to_be_removed)
        text_file.write_file(new_doc_entry.doc_file_path, new_doc_content.value)
        self.__stored_doc_entries_accessor.save_entry(new_doc_entry)
