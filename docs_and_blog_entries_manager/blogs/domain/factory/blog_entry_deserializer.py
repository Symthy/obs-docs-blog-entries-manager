from blogs.domain.entity import BlogEntry, PhotoEntries
from blogs.domain.value import BlogEntryId
from entries.domain.interface import IEntryDeserializer
from entries.domain.value import CategoryPath, EntryDateTime


class BlogEntryDeserializer(IEntryDeserializer):
    def deserialize(self, json_data: dict[str, any]) -> BlogEntry:
        return BlogEntry(
            BlogEntryId(json_data[BlogEntry.FIELD_ID]),
            json_data[BlogEntry.FIELD_TITLE],
            json_data[BlogEntry.FIELD_PAGE_URL],
            EntryDateTime(json_data[BlogEntry.FIELD_UPDATED_AT]),
            CategoryPath(json_data[BlogEntry.FIELD_CATEGORY_PATH]),
            json_data[BlogEntry.FIELD_CATEGORIES],
            PhotoEntries.deserialize(json_data[BlogEntry.FIELD_IMAGES]),
            json_data[BlogEntry.FIELD_PICKUP],
        )
