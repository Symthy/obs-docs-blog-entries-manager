from docs.domain.entity import DocEntry
from docs.domain.value import DocEntryId

from entries.domain.interface import IEntryDeserializer
from entries.domain.value import CategoryPath, EntryDateTime


class DocEntryDeserializer(IEntryDeserializer):
    def deserialize(self, json_data: dict[str, any]):
        return DocEntry(
            DocEntryId(json_data[DocEntry.FIELD_ID]),
            json_data[DocEntry.FIELD_TITLE],
            json_data[DocEntry.FIELD_DOC_FILE_NAME],
            CategoryPath(json_data[DocEntry.FIELD_CATEGORY_PATH]),
            json_data[DocEntry.FIELD_CATEGORIES],
            json_data[DocEntry.FIELD_PICKUP] if DocEntry.FIELD_PICKUP in json_data else False,
            EntryDateTime(json_data[DocEntry.FIELD_CREATED_AT]),
            EntryDateTime(json_data[DocEntry.FIELD_UPDATED_AT])
        )
