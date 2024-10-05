from assertpy import assert_that

from docs.infrastructure.doc_entry_restorer import DocEntryRestorer
from files.value.file_path import FilePath
from tests.docs.infrastructre._data.path_resolver import resolve_test_data_dir_path


class TestDocEntryRestorer:
    def setup_method(self):
        data_path = resolve_test_data_dir_path()
        self.__restorer = DocEntryRestorer(data_path.add_dir('docs'))

    def test_execute(self):
        doc_file_path = FilePath('Github', 'Github プロフィールのカスタマイズ.md')
        doc_entry = self.__restorer.restore(doc_file_path)
        assert_that(doc_entry.title).is_equal_to('Github プロフィールのカスタマイズ')
        assert_that(doc_entry.category_path.value.value).is_equal_to('Github')
        assert_that(doc_entry.categories).contains_only('profile')
        assert_that(doc_entry.pickup).is_false()
        assert_that(doc_entry.is_completed).is_true()
