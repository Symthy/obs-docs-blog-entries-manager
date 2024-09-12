from common.constants import DOCS_DIR_PATH
from docs.domain.entity import DocEntry
from docs.domain.factory import DocEntryBuilder
from docs.domain.value import DocEntryId
from docs.infrastructure.content import DocumentContentReader
from entries.domain.value import EntryDateTime
from files.value import DirectoryPath, FilePath
from stores.infrastructure import StoredEntryListHolder


class WorkingDocEntryRestorer:
    def __init__(self, doc_root_dir_path: DirectoryPath = DOCS_DIR_PATH):
        self.__internal = _InternalDocEntryRestorer(doc_root_dir_path)

    def restore(self, doc_entry_file_path: FilePath) -> DocEntry:
        return self.__internal.restore(doc_entry_file_path)


class DocEntryRestorer:
    def __init__(self, stored_doc_entry_list: StoredEntryListHolder, doc_root_dir_path: DirectoryPath = DOCS_DIR_PATH):
        self.__internal = _InternalDocEntryRestorer(doc_root_dir_path, stored_doc_entry_list)

    def restore(self, doc_entry_file_path: FilePath) -> DocEntry:
        return self.__internal.restore(doc_entry_file_path)


class _InternalDocEntryRestorer:
    def __init__(self, doc_root_dir_path: DirectoryPath = DOCS_DIR_PATH,
                 stored_doc_entry_list: StoredEntryListHolder = None):
        self.__doc_root_dir_path = doc_root_dir_path
        self.__stored_doc_entry_list = stored_doc_entry_list
        self.__doc_content_reader = DocumentContentReader()

    def restore(self, doc_entry_file_path: FilePath) -> DocEntry:
        doc_file_path = self.__doc_root_dir_path.join_file_path(doc_entry_file_path)
        content = self.__doc_content_reader.load(doc_file_path)
        created_at = doc_file_path.get_created_file_time()
        updated_at = doc_file_path.get_updated_file_time()
        entry_id = DocEntryId(created_at)
        pickup = self.__stored_doc_entry_list.is_pickup(entry_id) if self.__stored_doc_entry_list is not None else False
        return (DocEntryBuilder()
                .id(DocEntryId(created_at))
                .title(doc_file_path.get_file_name_without_ext())
                .doc_file_name(doc_file_path.get_file_name())
                .pickup(pickup)
                .category_path(content.category_path)
                .categories(*content.categories)
                .created_at(EntryDateTime(created_at))
                .updated_at(EntryDateTime(updated_at))
                .build())
