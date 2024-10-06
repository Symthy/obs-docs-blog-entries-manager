from blogs.domain.entity import BlogEntries, BlogEntry
from blogs.domain.value import BlogEntryId
from stores.infrastructure import StoredEntryListHolder

StoredBlogEntryListHolder = StoredEntryListHolder[BlogEntries, BlogEntry, BlogEntryId]