from common.constants import DOCS_DIR_PATH
from docs.domain.datasource.interface import IDocumentAccessor, StoredDocEntriesAccessor
from docs.domain.entity import DocEntries, DocEntry, DocumentDataset
from docs.domain.value import DocContent, DocEntryId, DocImages
from entries.domain.value import CategoryPath, EntryDateTime
from files import image_file
from files.value import FilePath, DirectoryPath
from .content.document_category_editor import DocumentCategoryEditor
from .content.document_content_saver import DocumentContentSaver
from .document_file_reader import DocumentFileReader


class DocumentFileAccessor(IDocumentAccessor):
    """
    ローカル記事への読み書き担当。読み込みはReaderに委譲
    """

    def __init__(self, stored_doc_entries_accessor: StoredDocEntriesAccessor,
                 document_file_reader: DocumentFileReader,
                 document_root_dir_path: DirectoryPath = DOCS_DIR_PATH):
        self.__document_root_dir_path = document_root_dir_path
        self.__stored_doc_entries_accessor = stored_doc_entries_accessor
        self.__document_reader = document_file_reader
        self.__document_saver = DocumentContentSaver()
        self.__document_category_editor = DocumentCategoryEditor(stored_doc_entries_accessor, document_root_dir_path)

    def find(self, doc_id: DocEntryId) -> DocumentDataset:
        """
        :raise: DocumentLoadingException
        """
        # delegate
        return self.__document_reader.find(doc_id)

    def restore(self, doc_entry_file_path: FilePath) -> DocEntry:
        """
        :raise: DocumentLoadingException
        """
        # delegate
        return self.__document_reader.restore(doc_entry_file_path)

    def extract_entries_with_blog_category(self) -> DocEntries:
        """
        :raise: DocumentLoadingException
        """
        # delegate
        return self.__document_reader.extract_entries_with_blog_category()

    def extract_entries_with_non_register(self) -> DocEntries:
        """
        :raise: DocumentLoadingException
        """
        # delegate
        return self.__document_reader.extract_entries_with_non_register()

    def save(self, doc_entry_dir_path: DirectoryPath, title: str, content: DocContent,
             images: DocImages | None = None) -> DocEntryId:
        """
        :raise: DocumentSavingException
        """
        doc_file_path = doc_entry_dir_path.add_file(f'{title}.md')
        self.__document_saver.save(doc_file_path, content)
        created_date_time = EntryDateTime(doc_file_path.get_created_file_time())
        doc_entry_id = DocEntryId(created_date_time.to_str_with_num_sequence())
        if images is None:
            return doc_entry_id
        for image in images.items:
            image_file.write(image.file_path, image.image_data)
        return doc_entry_id

    def save_summary(self, content: DocContent):
        """
        :raise: DocumentSavingException
        """
        summary_file_path = self.__document_root_dir_path.add_file('summary.md')
        self.__document_saver.save(summary_file_path, content)

    def insert_category(self, doc_id: DocEntryId, category_to_be_added: str) -> DocumentDataset:
        """
        :raise: DocumentSavingException
        """
        # delegate
        return self.__document_category_editor.insert_category(doc_id, category_to_be_added)

    def insert_category_path_to_content(self, doc_file_path: FilePath, category_path: CategoryPath) -> DocContent:
        """
        :raise: DocumentSavingException
        """
        # delegate
        return self.__document_category_editor.insert_category_path_to_content(doc_file_path, category_path)

    def delete_category(self, doc_id: DocEntryId, category_to_be_removed: str):
        """
        :raise: DocumentSavingException
        """
        # delegate
        self.__document_category_editor.delete_category(doc_id, category_to_be_removed)
