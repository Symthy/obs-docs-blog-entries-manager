from docs.domain.value import DocContent
from docs.infrastructure.exceptions.document_loading_exception import DocumentLoadingException
from files import text_file
from files.value import FilePath


class DocumentContentReader:

    @classmethod
    def load(cls, doc_file_path: FilePath) -> DocContent:
        try:
            content: str = text_file.read_file(doc_file_path)
            return DocContent(content)
        except Exception as e:
            raise DocumentLoadingException(doc_file_path, e)
