from entries.domain.value import CategoryPath


class FailedSaveEntryToBlogException(Exception):
    def __init__(self, title: str, category_path: CategoryPath):
        super().__init__(f"Failed to post to blog. (category path: {category_path}, title: {title})")
