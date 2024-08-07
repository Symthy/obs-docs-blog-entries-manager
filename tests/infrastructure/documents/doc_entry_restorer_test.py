import pytest
from assertpy import assert_that

from files import file_system
from infrastructure.documents.document_file_reader import DocumentFileReader
from tests.infrastructure.documents._data.path_resolver import resolve_test_data_dir_path


@pytest.fixture
def doc_entry_restorer():
    data_path = resolve_test_data_dir_path()
    return DocumentFileReader(file_system.join_path(data_path, 'docs'))


def test_execute(doc_entry_restorer):
    doc_file_path = file_system.join_path(resolve_test_data_dir_path(), 'docs', 'Github',
                                          'Github プロフィールのカスタマイズ.md')
    doc_entry = doc_entry_restorer.restore(doc_file_path)
    assert_that(doc_entry.title).is_equal_to('Github プロフィールのカスタマイズ')
    assert_that(doc_entry.category_path.value).is_equal_to('Github')
    assert_that(doc_entry.categories).contains_only('profile')
    assert_that(doc_entry.pickup).is_false()
    assert_that(doc_entry.is_completed).is_true()
