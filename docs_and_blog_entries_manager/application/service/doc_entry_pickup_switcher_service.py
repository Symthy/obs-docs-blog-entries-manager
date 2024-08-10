from typing import List

from domain.blogs.datasource.interface import StoredBlogEntriesModifier
from domain.docs.datasource.interface import StoredDocEntriesModifier
from domain.docs.value.doc_entry_id import DocEntryId
from domain.mappings.blog_to_doc_entry_mapping import BlogToDocEntryMapping


class DocEntryPickupSwitcherService:
    """
    指定したdocument(＆対応するblog記事)のpickupフラグON/OFF
    """

    def __init__(self, stored_doc_entries_modifier: StoredDocEntriesModifier,
                 stored_blog_entries_modifier: StoredBlogEntriesModifier,
                 blog_to_doc_entry_mapping: BlogToDocEntryMapping):
        self.__stored_doc_entries_modifier = stored_doc_entries_modifier
        self.__stored_blog_entries_modifier = stored_blog_entries_modifier
        self.__blog_to_doc_entry_mapping = blog_to_doc_entry_mapping

    def update_bulk(self, doc_entry_ids: List[DocEntryId], pickup: bool):
        for doc_entry_id in doc_entry_ids:
            self.__update_pickup(doc_entry_id, pickup)

    def update(self, doc_id: DocEntryId, pickup: bool):
        self.__update_pickup(doc_id, pickup)

    def __update_pickup(self, doc_entry_id: DocEntryId, pickup: bool):
        self.__stored_doc_entries_modifier.update_pickup(doc_entry_id, pickup)
        blog_entry_id = self.__blog_to_doc_entry_mapping.find_blog_entry_id(doc_entry_id)
        self.__stored_blog_entries_modifier.update_pickup(blog_entry_id, pickup)
