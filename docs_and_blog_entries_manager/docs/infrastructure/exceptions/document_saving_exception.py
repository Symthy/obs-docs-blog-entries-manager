from files.value import FilePath


class DocumentSavingException(Exception):
    def __init__(self, doc_file_path: FilePath, original_exception: Exception):
        super().__init__(f'Failed to save the document. (path: {doc_file_path} (detail: {original_exception})')
