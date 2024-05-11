from domain.docs.entity.doc_entry import DocEntry
from domain.docs.value.doc_content import DocContent
from domain.docs.value.doc_entry_id import DocEntryId
from domain.entries.values.entry_date_time import EntryDateTime
from files import file_system, text_file


class DocEntryRestorer:
    def __init__(self, document_root_dir_path):
        self.__document_root_dir_path = document_root_dir_path

    def execute(self, doc_entry_path) -> DocEntry:
        doc_file_path = self.__build_file_path(doc_entry_path)
        title = file_system.get_file_name_without_ext(doc_file_path)
        file_name = file_system.get_file_name(doc_file_path)
        content = DocContent(text_file.read_file(doc_file_path), doc_entry_path)
        category_path = content.category_path
        categories = content.categories
        created_at = file_system.get_created_file_time(doc_file_path)
        updated_at = file_system.get_updated_file_time(doc_file_path)
        doc_id = DocEntryId(created_at)
        return DocEntry(doc_id, title, file_name, category_path, categories, False, EntryDateTime(created_at),
                        EntryDateTime(updated_at))

    def __build_file_path(self, doc_entry_path: str) -> str:
        return file_system.join_path(self.__document_root_dir_path, doc_entry_path)
