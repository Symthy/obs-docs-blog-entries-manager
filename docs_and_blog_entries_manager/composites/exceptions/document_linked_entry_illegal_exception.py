from docs.domain.value import DocEntryId


class DocumentLinkedEntryIllegalException(Exception):
    def __init__(self, entry_id: DocEntryId):
        super().__init__(f"linked entry in the document contain non-exist entry. (doc entry id: {entry_id})")
