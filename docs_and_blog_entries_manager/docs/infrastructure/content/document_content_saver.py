from docs.domain.value import DocContent
from docs.infrastructure.exceptions.document_saving_exception import DocumentSavingException
from files import text_file
from files.value import FilePath


class DocumentContentSaver:

    @classmethod
    def save(cls, doc_file_path: FilePath, content: DocContent):
        try:
            text_file.write_file(doc_file_path, content.value)
        except Exception as e:
            raise DocumentSavingException(doc_file_path, e)
