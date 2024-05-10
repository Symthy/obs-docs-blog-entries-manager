from domain.docs.value.doc_content import DocContent
from files import text_file, file_system


class DocumentFileAccessor:
    def __init__(self, document_dir_path):
        self.__document_dir_path = document_dir_path

    def save(self, doc_entry_dir_path: str, file_name: str, content: str):
        text_file.write_file(file_system.join_path(doc_entry_dir_path, file_name), content)

    def load(self, doc_entry_dir_path: str, file_name: str) -> DocContent:
        content: str = text_file.read_file(file_system.join_path(doc_entry_dir_path, file_name))
        return DocContent(content, doc_entry_dir_path)
