from blogs.domain.value import BlogEntryId


class BlogEntryUpdateFailedException(Exception):
    def __init__(self, entry_id: BlogEntryId, e: Exception):
        self.original_exception = e
        super().__init__(f"Failed to update Blog entry (id: {entry_id.value}): {str(e)}")
