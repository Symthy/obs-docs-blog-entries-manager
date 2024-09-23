from common.constants import BLOG_CATEGORY, DOCS_DIR_PATH
from docs.domain.datasource.interface import StoredDocEntriesAccessor
from docs.domain.entity import DocumentDataset
from docs.domain.value import DocContent, DocEntryId
from docs.infrastructure.content.document_content_saver import DocumentContentSaver
from docs.infrastructure.file.document_file_finder import DocumentFileFinder
from entries.domain.value import CategoryPath
from files import text_file
from files.value import FilePath, DirectoryPath


class DocumentCategoryEditor:
    def __init__(self, stored_doc_entries_accessor: StoredDocEntriesAccessor,
                 doc_root_dir_path: DirectoryPath = DOCS_DIR_PATH):
        self.__stored_doc_entries_accessor = stored_doc_entries_accessor
        self.__document_file_finder = DocumentFileFinder(stored_doc_entries_accessor, doc_root_dir_path)
        self.__document_content_saver = DocumentContentSaver()

    def insert_category(self, doc_id: DocEntryId, category_to_be_added: str) -> DocumentDataset:
        """
        :raise: DocumentSavingException
        """
        doc_dataset = self.__document_file_finder.find(doc_id)
        new_doc_content = self.__insert_category_to_content(doc_dataset.doc_entry.doc_file_path,
                                                            doc_dataset.doc_content, category_to_be_added)
        new_doc_entry = doc_dataset.doc_entry.insert_category(category_to_be_added)
        self.__stored_doc_entries_accessor.save_entry(new_doc_entry)
        return DocumentDataset(new_doc_entry, new_doc_content)

    def __insert_category_to_content(self, doc_file_path: FilePath, content: DocContent, category: str) -> DocContent:
        """
        :raise: DocumentSavingException
        """
        if category == BLOG_CATEGORY and content.contains_category(BLOG_CATEGORY):
            return content
        updated_content = content.add_category(category)
        self.__document_content_saver.save(doc_file_path, updated_content)
        return updated_content

    def insert_category_path(self, doc_file_path: FilePath, category_path: CategoryPath) -> DocContent:
        """
        :raise: DocumentSavingException
        """
        content = DocContent(text_file.read_file(doc_file_path))
        updated_content = content.update_category_path(category_path)
        self.__document_content_saver.save(doc_file_path, updated_content)
        return content

    def delete_category(self, doc_id: DocEntryId, category_to_be_removed: str):
        """
        :raise: DocumentSavingException
        """
        doc_dataset = self.__document_file_finder.find(doc_id)
        new_doc_entry = doc_dataset.doc_entry.remove_category(category_to_be_removed)
        new_doc_content = doc_dataset.doc_content.remove_category(category_to_be_removed)
        self.__document_content_saver.save(new_doc_entry.doc_file_path, new_doc_content)
        self.__stored_doc_entries_accessor.save_entry(new_doc_entry)
