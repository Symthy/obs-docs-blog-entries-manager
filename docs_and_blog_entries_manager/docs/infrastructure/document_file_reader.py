from common.constants import DOCS_DIR_PATH
from docs.domain.datasource.interface import IDocumentReader, StoredDocEntriesAccessor
from docs.domain.entity import DocEntries, DocEntry, DocumentDataset
from docs.domain.value import DocEntryId
from docs.infrastructure.doc_entry_restorer import DocEntryRestorer
from docs.infrastructure.file import AllDocumentPathResolver
from docs.infrastructure.file.document_file_finder import DocumentFileFinder
from docs.infrastructure.types import ReadableDocEntryListHolder
from files.value import DirectoryPath, FilePath


class DocumentFileReader(IDocumentReader):

    def __init__(self, stored_doc_entries_accessor: StoredDocEntriesAccessor,
                 stored_doc_entry_list: ReadableDocEntryListHolder,
                 all_document_path_resolver: AllDocumentPathResolver,
                 doc_root_dir_path: DirectoryPath = DOCS_DIR_PATH):
        self.__stored_doc_entries_accessor = stored_doc_entries_accessor
        self.__stored_doc_entry_list = stored_doc_entry_list
        self.__doc_entry_restorer = DocEntryRestorer(doc_root_dir_path, stored_doc_entry_list)
        self.__all_document_path_resolver = all_document_path_resolver
        self.__document_file_finder = DocumentFileFinder(stored_doc_entries_accessor, doc_root_dir_path)

    def find(self, doc_id: DocEntryId) -> DocumentDataset:
        """
        :raise: DocumentLoadingException
        """
        # delegate
        return self.__document_file_finder.find(doc_id)

    def restore(self, doc_entry_file_path: FilePath) -> DocEntry:
        """
        :raise: DocumentLoadingException
        """
        # delegate
        return self.__doc_entry_restorer.restore(doc_entry_file_path)

    def extract_entries_with_blog_category(self) -> DocEntries:
        """
        :raises: DocumentLoadingException
        """
        added_blog_category_entries = []
        doc_entries = self.__stored_doc_entries_accessor.load_entries()
        for old_doc_entry in doc_entries.items_filtered_non_blog_category():
            current_doc_entry = self.restore(old_doc_entry.doc_file_path)
            current_doc_entry.contains_blog_category()
            added_blog_category_entries.append(current_doc_entry)
        return DocEntries(added_blog_category_entries)

    def extract_entries_with_non_register(self) -> DocEntries:
        """
        :raise: DocumentLoadingException
        """
        doc_id_to_path: dict[DocEntryId, str] = self.__all_document_path_resolver.resolve()
        doc_entries: list[DocEntry] = []
        for doc_id, doc_entry_path in doc_id_to_path:
            if not self.__stored_doc_entry_list.exist_id(doc_id):
                doc_entries.append(self.restore(doc_entry_path))
        return DocEntries(doc_entries)
