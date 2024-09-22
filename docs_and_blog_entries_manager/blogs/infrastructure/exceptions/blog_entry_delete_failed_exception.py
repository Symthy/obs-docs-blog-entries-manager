from blogs.domain.value import BlogEntryId


class BlogEntryDeleteFailedException(Exception):
    def __init__(self, entry_id: BlogEntryId, e: Exception):
        self.original_exception = e
        super().__init__(f"Failed to delete Blog entry (id: {entry_id.value}): {str(e)}")
