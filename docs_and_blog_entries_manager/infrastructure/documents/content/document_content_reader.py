from domain.docs.value.doc_content import DocContent
from files import text_file
from files.value.file_path import FilePath


class DocumentContentReader:

    @classmethod
    def load(cls, doc_file_path: FilePath) -> DocContent:
        content: str = text_file.read_file(doc_file_path)
        return DocContent(content)
