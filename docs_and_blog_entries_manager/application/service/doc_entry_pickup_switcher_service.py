from typing import List

from domain.docs.types import StoredDocEntriesAccessor
from domain.docs.value.doc_entry_id import DocEntryId
from infrastructure.store.blog_to_doc_entry_mapping import BlogToDocEntryMapping
from infrastructure.types import StoredBlogEntriesAccessor


class DocEntryPickupSwitcherService:
    """
    指定したdocument(＆対応するblog記事)のpickupフラグON/OFF
    """

    def __init__(self, stored_doc_entries_accessor: StoredDocEntriesAccessor,
                 stored_blog_entries_accessor: StoredBlogEntriesAccessor,
                 blog_to_doc_entry_mapping: BlogToDocEntryMapping):
        self.__stored_doc_entries_accessor = stored_doc_entries_accessor
        self.__stored_blog_entries_accessor = stored_blog_entries_accessor
        self.__blog_to_doc_entry_mapping = blog_to_doc_entry_mapping

    def update_bulk(self, doc_entry_ids: List[DocEntryId], pickup: bool):
        for doc_entry_id in doc_entry_ids:
            self.__update_pickup(doc_entry_id, pickup)

    def update(self, doc_id: DocEntryId, pickup: bool):
        self.__update_pickup(doc_id, pickup)

    def __update_pickup(self, doc_entry_id: DocEntryId, pickup: bool):
        self.__stored_doc_entries_accessor.update_pickup(doc_entry_id, pickup)
        blog_entry_id = self.__blog_to_doc_entry_mapping.find_blog_entry_id(doc_entry_id)
        self.__stored_blog_entries_accessor.update_pickup(blog_entry_id, pickup)
