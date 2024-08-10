from common.constants import DOCS_DIR_PATH
from domain.docs.entity.doc_entry import DocEntry
from domain.docs.entity.factory.doc_entry_builder import DocEntryBuilder
from domain.docs.value.doc_entry_id import DocEntryId
from domain.entries.values.entry_date_time import EntryDateTime
from files import file_system
from infrastructure.documents.content.document_content_reader import DocumentContentReader
from infrastructure.store.stored_entry_list_holder import StoredEntryListHolder


class WorkingDocEntryRestorer:
    def __init__(self, doc_root_dir_path: str = DOCS_DIR_PATH):
        self.__internal = _InternalDocEntryRestorer(doc_root_dir_path)

    def restore(self, doc_entry_file_path: str) -> DocEntry:
        return self.__internal.restore(doc_entry_file_path)


class DocEntryRestorer:
    def __init__(self, stored_doc_entry_list: StoredEntryListHolder, doc_root_dir_path: str = DOCS_DIR_PATH):
        self.__internal = _InternalDocEntryRestorer(doc_root_dir_path, stored_doc_entry_list)

    def restore(self, doc_entry_file_path: str) -> DocEntry:
        return self.__internal.restore(doc_entry_file_path)


class _InternalDocEntryRestorer:
    def __init__(self, doc_root_dir_path: str = DOCS_DIR_PATH, stored_doc_entry_list: StoredEntryListHolder = None):
        self.__doc_root_dir_path = doc_root_dir_path
        self.__stored_doc_entry_list = stored_doc_entry_list
        self.__doc_content_reader = DocumentContentReader()

    def restore(self, doc_entry_file_path: str) -> DocEntry:
        doc_file_path = file_system.join_path(self.__doc_root_dir_path, doc_entry_file_path)
        content = self.__doc_content_reader.load(doc_file_path)
        created_at = file_system.get_created_file_time(doc_file_path)
        updated_at = file_system.get_updated_file_time(doc_file_path)
        entry_id = DocEntryId(created_at)
        pickup = self.__stored_doc_entry_list.is_pickup(entry_id) if self.__stored_doc_entry_list is not None else False
        return (DocEntryBuilder()
                .id(DocEntryId(created_at))
                .title(file_system.get_file_name_without_ext(doc_file_path))
                .doc_file_name(file_system.get_file_name(doc_file_path))
                .pickup(pickup)
                .category_path(content.category_path)
                .categories(*content.categories)
                .created_at(EntryDateTime(created_at))
                .updated_at(EntryDateTime(updated_at))
                .build())
