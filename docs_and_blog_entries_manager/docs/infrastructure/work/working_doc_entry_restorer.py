from common.constants import DOCS_DIR_PATH
from docs.domain.entity import DocEntry
from docs.domain.factory import DocEntryBuilder
from docs.domain.value import DocEntryId
from docs.infrastructure.content.document_content_reader import DocumentContentReader
from entries.domain.value import CategoryPath, EntryDateTime
from files.value import DirectoryPath, FilePath


class WorkingDocEntryRestorer:
    def __init__(self, doc_root_dir_path: DirectoryPath = DOCS_DIR_PATH):
        self.__doc_root_dir_path = doc_root_dir_path
        self.__doc_content_reader = DocumentContentReader()

    def restore(self, doc_entry_file_path: FilePath) -> DocEntry:
        """
        :raise: DocumentLoadingException
        """
        doc_file_path = self.__doc_root_dir_path.join_file_path(doc_entry_file_path)
        content = self.__doc_content_reader.load(doc_file_path)
        if content.category_path is None:
            category_path = CategoryPath.non_category()
            content.update_category_path(category_path)
        created_at = doc_file_path.get_created_file_time()
        updated_at = doc_file_path.get_updated_file_time()
        return (DocEntryBuilder()
                .id(DocEntryId(created_at))
                .title(doc_file_path.get_file_name_without_ext())
                .doc_file_name(doc_file_path.get_file_name())
                .pickup(False)
                .category_path(content.category_path)
                .categories(*content.categories)
                .created_at(EntryDateTime(created_at))
                .updated_at(EntryDateTime(updated_at))
                .build())
