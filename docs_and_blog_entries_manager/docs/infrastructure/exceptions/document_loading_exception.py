from files.value import FilePath


class DocumentLoadingException(Exception):
    def __init__(self, doc_file_path: FilePath, original_exception: Exception):
        super().__init__(f'Failed to load the document. (path: {doc_file_path} (detail: {original_exception})')
