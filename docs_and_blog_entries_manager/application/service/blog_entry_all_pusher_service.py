from typing import List

from application.service.blog_entry_pusher_service import BlogEntryPusherService
from domain.docs.entity.doc_entry import DocEntry
from infrastructure.types import StoredDocEntriesAccessor


class BlogEntryAllPusherService:
    def __init__(self, stored_doc_entries_accessor: StoredDocEntriesAccessor,
                 blog_entry_pusher: BlogEntryPusherService):
        self.__stored_doc_entries_accessor = stored_doc_entries_accessor
        self.__blog_entry_pusher = blog_entry_pusher

    def execute(self):
        doc_entries_has_blog_category: List[DocEntry] \
            = self.__stored_doc_entries_accessor.load_entries().items_filtered_blog_category
        for doc_entry in doc_entries_has_blog_category:
            self.__blog_entry_pusher.execute(doc_entry.id)
