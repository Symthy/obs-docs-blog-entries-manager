from domain.blogs.entity.blog_entry import BlogEntry
from domain.blogs.entity.photo.photo_entries import PhotoEntries
from domain.blogs.value.blog_entry_id import BlogEntryId
from domain.entries.interface import IEntryDeserializer
from domain.entries.values.category_path import CategoryPath
from domain.entries.values.entry_date_time import EntryDateTime


class BlogEntryDeserializer(IEntryDeserializer):
    def deserialize(self, json_data: dict[str, any]) -> BlogEntry:
        return BlogEntry(
            BlogEntryId(json_data[BlogEntry.FIELD_ID]),
            json_data[BlogEntry.FIELD_TITLE],
            json_data[BlogEntry.FIELD_PAGE_URL],
            EntryDateTime(json_data[BlogEntry.FIELD_UPDATED_AT]),
            CategoryPath(json_data[BlogEntry.FIELD_CATEGORY_PATH]),
            json_data[BlogEntry.FIELD_CATEGORIES],
            PhotoEntries.deserialize(json_data[BlogEntry.FIELD_DOC_IMAGES])
        )
