from domain.docs.entity.doc_entry import DocEntry
from domain.docs.value.doc_entry_id import DocEntryId
from domain.entries.interface import IEntryDeserializer
from domain.entries.values.category_path import CategoryPath
from domain.entries.values.entry_date_time import EntryDateTime


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
