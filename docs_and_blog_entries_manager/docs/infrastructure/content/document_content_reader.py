from docs.domain.value import DocContent
from files import text_file
from files.value import FilePath


class DocumentContentReader:

    @classmethod
    def load(cls, doc_file_path: FilePath) -> DocContent:
        content: str = text_file.read_file(doc_file_path)
        return DocContent(content)
