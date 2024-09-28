from files.value import FilePath


class FailedSaveEntryToBlogException(Exception):
    def __init__(self, file_path: FilePath):
        super().__init__(f"Failed to post to blog. (document path: {file_path})")


s
