from domain.docs.value.doc_content import DocContent
from files import file_system, text_file


class DocumentContentReader:

    @classmethod
    def load(cls, doc_file_path: str) -> DocContent:
        content: str = text_file.read_file(doc_file_path)
        doc_dir_path = file_system.get_dir_path_from_file_path(doc_file_path)
        return DocContent(content, doc_dir_path)
