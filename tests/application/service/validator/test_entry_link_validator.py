from assertpy import assert_that

from application.service.validator.entry_link_validator import EntryLinkValidator
from domain.docs.value.doc_entry_id import DocEntryId
from files.file_system import join_path
from infrastructure.documents.document_file_reader import DocumentFileReader
from infrastructure.store.blog_to_doc_entry_mapping import BlogToDocEntryMapping
from infrastructure.store.factory.stored_entries_accessor_factory import StoredEntriesAccessorFactory
from infrastructure.store.stored_entry_title_finder import StoredEntryTitleFinder
from tests.application.service.validator._data.path_resolver import resolve_test_data_dir_path


class TestEntryLinkValidator:
    def setup_method(self):
        dir_path = resolve_test_data_dir_path()
        store_dir = join_path(dir_path, 'store')
        docs_dir = join_path(dir_path, 'docs')
        blog_to_doc_mapping = BlogToDocEntryMapping(join_path(store_dir, 'blog_to_doc_mapping.json'))
        stored_doc_entries_accessor = StoredEntriesAccessorFactory(store_dir).build_for_doc()
        document_reader = DocumentFileReader(docs_dir, stored_doc_entries_accessor)
        self.__entry_title_finder = EntryLinkValidator(StoredEntryTitleFinder(stored_doc_entries_accessor),
                                                       blog_to_doc_mapping, document_reader)

    def test_validate_when_nothing_doc_return_false(self):
        actual = self.__entry_title_finder.validate(DocEntryId('20240701120000111111'))
        assert_that(actual).is_false()

    def test_validate_return_true(self):
        actual = self.__entry_title_finder.validate(DocEntryId('20240701120000222222'))
        assert_that(actual).is_true()

    def test_validate_when_nothing_blog_return_false(self):
        actual = self.__entry_title_finder.validate(DocEntryId('20240701120000333333'))
        assert_that(actual).is_false()
