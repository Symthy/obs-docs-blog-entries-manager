import pytest
from assertpy import assert_that
from mock import mock

from domain.docs.entity.factory.doc_entry_builder import DocEntryBuilder
from domain.docs.value.doc_entry_id import DocEntryId
from domain.entries.values.category_path import CategoryPath
from domain.entries.values.entry_date_time import EntryDateTime
from files import file_system
from infrastructure.documents.document_file_accessor import DocumentFileAccessor
from infrastructure.store.factory.stored_entry_list_deserializer import StoredDocEntryListDeserializer
from infrastructure.types import StoredDocEntriesAccessor
from tests.infrastructure.documents._data.path_resolver import resolve_test_data_dir_path


@pytest.fixture
def document_file_accessor():
    data_path = resolve_test_data_dir_path()
    docs_dir_path = file_system.join_path(data_path, 'docs')
    doc_entry = (DocEntryBuilder().id(DocEntryId('20240501000000'))
                 .category_path(CategoryPath('Github'))
                 .categories('profile')
                 .title('Github プロフィールのカスタマイズ')
                 .doc_file_name('Github プロフィールのカスタマイズ.md')
                 .pickup(False)
                 .created_at(EntryDateTime())
                 .updated_at(EntryDateTime())
                 .build())
    accessor_mock = mock.MagicMock(StoredDocEntriesAccessor)
    accessor_mock.load_entry.return_value = doc_entry
    entry_list = StoredDocEntryListDeserializer(file_system.join_path(data_path, 'doc_entry_list.json')).deserialize()
    return DocumentFileAccessor(docs_dir_path, entry_list, accessor_mock)


def test_find_document(document_file_accessor):
    doc_dataset = document_file_accessor.find_document(DocEntryId('20240501000000'))
    assert_that(doc_dataset.doc_entry.id.value).is_equal_to('20240501000000')
    assert_that(doc_dataset.doc_content.category_path.value).is_equal_to('Github')
    assert_that(doc_dataset.doc_content.image_paths_from_doc_file).contains_only('images/github-profile-summary.png')
