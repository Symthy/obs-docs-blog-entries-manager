from domain.blogs.entity.blog_entries import BlogEntries
from domain.blogs.entity.blog_entry import BlogEntry
from domain.blogs.value.blog_entry_id import BlogEntryId
from domain.docs.entity.doc_entries import DocEntries
from domain.docs.entity.doc_entry import DocEntry
from domain.docs.value.doc_entry_id import DocEntryId
from infrastructure.store.stored_entries_accessor import StoredEntriesAccessor

StoredDocEntriesAccessor = StoredEntriesAccessor[DocEntries, DocEntry, DocEntryId]
StoredBlogEntriesAccessor = StoredEntriesAccessor[BlogEntries, BlogEntry, BlogEntryId]
