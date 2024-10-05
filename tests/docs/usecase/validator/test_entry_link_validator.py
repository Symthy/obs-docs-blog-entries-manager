import mock
from assertpy import assert_that

from composites.entity.blog_to_doc_entry_mapping import BlogToDocEntryMapping
from docs.domain.value.doc_entry_id import DocEntryId
from docs.infrastructure.document_file_reader import DocumentFileReader
from docs.infrastructure.factory import StoredDocEntriesAccessorFactory, StoredDocEntryListDeserializer
from docs.infrastructure.file.all_document_path_resolver import AllDocumentPathResolver
from docs.usecase.validator.doc_entry_link_validator import DocEntryLinkValidator
from stores.infrastructure.stored_entry_title_finder import StoredEntryTitleFinder
from tests.docs.usecase.validator._data.path_resolver import resolve_test_data_dir_path


class TestEntryLinkValidator:
    def setup_method(self):
        dir_path = resolve_test_data_dir_path()
        store_dir = dir_path.add_dir('store')
        docs_dir = dir_path.add_dir('docs')
        blog_to_doc_mapping = BlogToDocEntryMapping(store_dir.add_file('blog_to_doc_mapping.json'))
        doc_entry_list = StoredDocEntryListDeserializer(store_dir.add_file('doc_entry_list.json')).deserialize()
        stored_doc_entries_accessor = StoredDocEntriesAccessorFactory(store_dir).build(doc_entry_list)
        resolver_mock = mock.MagicMock(AllDocumentPathResolver)
        document_reader = DocumentFileReader(stored_doc_entries_accessor, doc_entry_list, resolver_mock, docs_dir)
        self.__entry_title_validator = DocEntryLinkValidator(StoredEntryTitleFinder(stored_doc_entries_accessor),
                                                             blog_to_doc_mapping, document_reader)

    def test_validate_when_nothing_doc_return_false(self):
        actual = self.__entry_title_validator.validate(DocEntryId('20240701120000111111'))
        assert_that(actual).is_false()

    def test_validate_return_true(self):
        actual = self.__entry_title_validator.validate(DocEntryId('20240701120000222222'))
        assert_that(actual).is_true()

    def test_validate_when_nothing_blog_return_false(self):
        actual = self.__entry_title_validator.validate(DocEntryId('20240701120000333333'))
        assert_that(actual).is_false()
