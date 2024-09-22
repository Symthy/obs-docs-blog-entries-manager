from blogs.domain.value import BlogEntryId


class BlogEntryFindFailedException(Exception):
    def __init__(self, entry_id: BlogEntryId, e: Exception):
        self.original_exception = e
        super().__init__(f"Failed to get Blog entry (id: {entry_id.value})  {str(e)}")
