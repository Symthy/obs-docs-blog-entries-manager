from domain.blogs.value.blog_entry_id import BlogEntryId
from infrastructure.store.factory.stored_entry_list_deserializer import StoredEntryListDeserializer


def test_build():
    input_data = {
        "updated_at": "2024-05-18T13:45:02+0900",
        "entries": {
            "20240501000000": "False",
            "20240502000000": "True",
            "20240503000000": "False",
            "20240504000000": "True",
            "20240505000000": "False"
        }
    }
    entry_list = StoredEntryListDeserializer(BlogEntryId.new_instance).build(input_data)
    assert entry_list.update_at == "2024-05-18T13:45:02+0900"
    assert entry_list.entries[BlogEntryId("20240501000000")] is False
    assert entry_list.entries[BlogEntryId("20240502000000")] is True
    assert entry_list.entries[BlogEntryId("20240503000000")] is False
    assert entry_list.entries[BlogEntryId("20240504000000")] is True
    assert entry_list.entries[BlogEntryId("20240505000000")] is False
