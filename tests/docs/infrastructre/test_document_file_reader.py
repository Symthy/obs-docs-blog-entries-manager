from assertpy import assert_that
from mock import mock

from docs.domain.datasource.interface import StoredDocEntriesAccessor
from docs.domain.factory.doc_entry_builder import DocEntryBuilder
from docs.domain.value.doc_entry_id import DocEntryId
from docs.infrastructure.document_file_reader import DocumentFileReader
from docs.infrastructure.file.all_document_path_resolver import AllDocumentPathResolver
from entries.domain.value.category_path import CategoryPath
from entries.domain.value.entry_date_time import EntryDateTime
from stores.factory.stored_entry_list_deserializer import StoredDocEntryListDeserializer
from tests.docs.infrastructre._data.path_resolver import resolve_test_data_dir_path


class TestDocumentFileReader:
    def setup_method(self):
        data_path = resolve_test_data_dir_path()
        docs_dir_path = data_path.add_dir('docs')
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
        resolver_mock = mock.MagicMock(AllDocumentPathResolver)
        entry_list = StoredDocEntryListDeserializer(data_path.add_file('doc_entry_list.json')).deserialize()
        self.__reader = DocumentFileReader(accessor_mock, entry_list, resolver_mock, docs_dir_path)

    def test_find(self):
        doc_dataset = self.__reader.find(DocEntryId('20240501000000'))
        assert_that(doc_dataset.doc_entry.id.value).is_equal_to('20240501000000')
        assert_that(doc_dataset.doc_content.category_path.value.value).is_equal_to('Github')
        assert_that(doc_dataset.doc_content.image_paths_from_doc_files).contains_only(
            'images/github-profile-summary.png')
