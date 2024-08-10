from common.constants import BLOG_CATEGORY, DOCS_DIR_PATH
from domain.docs.datasources.interface import IDocumentAccessor
from domain.docs.datasources.model.document_dataset import DocumentDataset
from domain.docs.entity.doc_entries import DocEntries
from domain.docs.entity.doc_entry import DocEntry
from domain.docs.entity.image.doc_images import DocImages
from domain.docs.value.doc_content import DocContent
from domain.docs.value.doc_entry_id import DocEntryId
from domain.entries.values.category_path import CategoryPath
from domain.entries.values.entry_date_time import EntryDateTime
from files import text_file, file_system, image_file
from infrastructure.documents.document_file_reader import DocumentFileReader
from infrastructure.store.stored_entry_list_holder import StoredEntryListHolder
from infrastructure.types import StoredDocEntriesAccessor


class DocumentFileAccessor(IDocumentAccessor):

    def __init__(self, stored_doc_entries_accessor: StoredDocEntriesAccessor,
                 stored_entry_list: StoredEntryListHolder,
                 document_root_dir_path: str = DOCS_DIR_PATH,
                 document_file_reader: DocumentFileReader = None):
        self.__document_root_dir_path = document_root_dir_path
        self.__stored_doc_entries_accessor = stored_doc_entries_accessor
        if document_file_reader is None:
            self.__document_reader = DocumentFileReader(stored_doc_entries_accessor, stored_entry_list,
                                                        document_root_dir_path)
        else:
            self.__document_reader = document_file_reader

    def find(self, doc_id: DocEntryId) -> DocumentDataset:
        return self.__document_reader.find(doc_id)

    def restore(self, doc_entry_file_path: str) -> DocEntry:
        return self.__document_reader.restore(doc_entry_file_path)

    def extract_entries_with_blog_category(self) -> DocEntries:
        return self.__document_reader.extract_entries_with_blog_category()

    def extract_entries_with_non_register(self) -> DocEntries:
        return self.__document_reader.extract_entries_with_non_register()

    @classmethod
    def save(cls, doc_entry_dir_path: str, title: str, content: DocContent,
             images: DocImages | None = None) -> DocEntryId:
        doc_file_path = file_system.join_path(doc_entry_dir_path, f'{title}.md')
        text_file.write_file(doc_file_path, content.value)
        created_date_time = EntryDateTime(file_system.get_created_file_time(doc_file_path))
        doc_entry_id = DocEntryId(created_date_time.to_str_with_num_sequence())
        if images is None:
            return doc_entry_id
        for image in images.items:
            image_file.write(image.file_path, image.image_data)
        return doc_entry_id

    def save_summary(self, content: DocContent):
        summary_file_path = file_system.join_path(self.__document_root_dir_path, 'summary.md')
        text_file.write_file(summary_file_path, content.value)

    def insert_category(self, doc_id: DocEntryId, category_to_be_added: str) -> DocumentDataset:
        doc_dataset = self.__document_reader.find(doc_id)
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
        content = DocContent(text_file.read_file(doc_file_path), file_system.get_dir_path_from_file_path(doc_file_path))
        text_file.write_file(doc_file_path, content.update_category_path(category_path).value)
        return content

    def delete_category(self, doc_id: DocEntryId, category_to_be_removed: str):
        doc_dataset = self.__document_reader.find(doc_id)
        new_doc_entry = doc_dataset.doc_entry.remove_category(category_to_be_removed)
        new_doc_content = doc_dataset.doc_content.remove_category(category_to_be_removed)
        text_file.write_file(new_doc_entry.doc_file_path, new_doc_content.value)
        self.__stored_doc_entries_accessor.save_entry(new_doc_entry)
