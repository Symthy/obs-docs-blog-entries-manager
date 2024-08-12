from assertpy import assert_that

from infrastructure.documents.doc_entry_restorer import _InternalDocEntryRestorer
from tests.infrastructure.documents._data.path_resolver import resolve_test_data_dir_path


class TestDocEntryRestorer:
    def setup_method(self):
        self.__data_path = resolve_test_data_dir_path()
        self.__restorer = _InternalDocEntryRestorer(self.__data_path.add_dir('docs'))

    def test_execute(self):
        doc_file_path = self.__data_path.add_file('docs/Github/Github プロフィールのカスタマイズ.md')
        doc_entry = self.__restorer.restore(doc_file_path)
        assert_that(doc_entry.title).is_equal_to('Github プロフィールのカスタマイズ')
        assert_that(doc_entry.category_path.value.value).is_equal_to('Github')
        assert_that(doc_entry.categories).contains_only('profile')
        assert_that(doc_entry.pickup).is_false()
        assert_that(doc_entry.is_completed).is_true()
