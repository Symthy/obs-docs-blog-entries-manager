class BlogEntryFindAllFailedException(Exception):
    def __init__(self, e: Exception):
        self.original_exception = e
        super().__init__(f"Failed to get all Blog entries: {str(e)}")
