from files.value import FilePath


class DocumentMovingException(Exception):
    def __init__(self, from_file_path: FilePath, to_file_path: FilePath, original_exception: Exception):
        super().__init__(f'Failed to move from {from_file_path} to {to_file_path} (detail: {original_exception})')
