import pytest
from assertpy import assert_that

from entries.domain.entity.category_tree_definition import CategoryTreeDefinition
from entries.domain.entity.entries_tree_roots import EntriesTreeRoots
from entries.domain.factory.entries_tree_roots_restorer import EntriesTreeRootsRestorer
from entries.domain.interface import IEntries
from entries.domain.value.category_path import CategoryPath
from stores.infrastructure.stored_entries_accessor import StoredEntriesAccessor


@pytest.fixture
def input_mocks(mocker):
    mock_entries0 = mocker.Mock(spec=IEntries)
    mock_entries0.is_empty.return_value = False
    mock_entries1 = mocker.Mock(spec=IEntries)
    mock_entries1.is_empty.return_value = False
    mock_entries2 = mocker.Mock(spec=IEntries)
    mock_entries2.is_empty.return_value = False
    mock_entries3 = mocker.Mock(spec=IEntries)
    mock_entries3.is_empty.return_value = False
    mock_entries4 = mocker.Mock(spec=IEntries)
    mock_entries4.is_empty.return_value = False
    mock_entries5 = mocker.Mock(spec=IEntries)
    mock_entries5.is_empty.return_value = False
    mock_entries6 = mocker.Mock(spec=IEntries)
    mock_entries6.is_empty.return_value = False
    mock_entries7 = mocker.Mock(spec=IEntries)
    mock_entries7.is_empty.return_value = False

    mock_category_tree_def = mocker.Mock(spec=CategoryTreeDefinition)
    mock_category_tree_def.category_full_paths = [
        CategoryPath('Backend/DB/SQL'),
        CategoryPath('Frontend/JS/React'),
        CategoryPath('Frontend/JS/React/Next'),
        CategoryPath('Frontend/JS/Vue'),
    ]

    mock_stored_entries_accessor = mocker.Mock(spec=StoredEntriesAccessor)
    mock_stored_entries_accessor.load_entries_by_category_path.side_effect = lambda path: {
        CategoryPath('Backend/DB/SQL'): mock_entries0,
        CategoryPath('Backend/DB'): mock_entries1,
        CategoryPath('Backend'): mock_entries2,
        CategoryPath('Frontend/JS/React/Next'): mock_entries3,
        CategoryPath('Frontend/JS/React'): mock_entries4,
        CategoryPath('Frontend/JS/Vue'): mock_entries5,
        CategoryPath('Frontend/JS'): mock_entries6,
        CategoryPath('Frontend'): mock_entries7
    }.get(path, None)
    return {
        CategoryTreeDefinition.__name__: mock_category_tree_def,
        StoredEntriesAccessor.__name__: mock_stored_entries_accessor,
        'mock_entries': [mock_entries0, mock_entries1, mock_entries2, mock_entries3, mock_entries4, mock_entries5,
                         mock_entries6, mock_entries7]
    }


class TestEntriesTreeRootsRestorer:

    def test_build_all_category_path_to_entries(self, input_mocks):
        restorer = EntriesTreeRootsRestorer(
            input_mocks[CategoryTreeDefinition.__name__],
            input_mocks[StoredEntriesAccessor.__name__])
        actual: dict[CategoryPath, IEntries] = restorer.build_all_category_path_to_entries_for_testing()
        assert_that(actual.get(CategoryPath('Backend/DB/SQL'))).is_equal_to(input_mocks['mock_entries'][0])
        assert_that(actual.get(CategoryPath('Backend/DB'))).is_equal_to(input_mocks['mock_entries'][1])
        assert_that(actual.get(CategoryPath('Backend'))).is_equal_to(input_mocks['mock_entries'][2])
        assert_that(actual.get(CategoryPath('Frontend/JS/React/Next'))).is_equal_to(input_mocks['mock_entries'][3])
        assert_that(actual.get(CategoryPath('Frontend/JS/React'))).is_equal_to(input_mocks['mock_entries'][4])
        assert_that(actual.get(CategoryPath('Frontend/JS/Vue'))).is_equal_to(input_mocks['mock_entries'][5])
        assert_that(actual.get(CategoryPath('Frontend/JS'))).is_equal_to(input_mocks['mock_entries'][6])
        assert_that(actual.get(CategoryPath('Frontend'))).is_equal_to(input_mocks['mock_entries'][7])

    def test_execute(self, input_mocks):
        restorer = EntriesTreeRootsRestorer(
            input_mocks[CategoryTreeDefinition.__name__],
            input_mocks[StoredEntriesAccessor.__name__])
        actual: EntriesTreeRoots = restorer.execute()

        assert_that(actual.root_num()).is_equal_to(2)
        assert_that(actual.get_root_tree(CategoryPath('Backend')).entries).is_equal_to(input_mocks['mock_entries'][2])
        assert_that(actual.get_root_tree(CategoryPath('Frontend')).entries).is_equal_to(input_mocks['mock_entries'][7])
        assert_that(actual.search_tree(CategoryPath('Frontend/JS')).children).is_length(2)
        assert_that(actual.search_tree(CategoryPath('Frontend/JS')).child_category_paths).contains(
            CategoryPath('Frontend/JS/React'))
        assert_that(actual.search_tree(CategoryPath('Frontend/JS')).child_category_paths).contains(
            CategoryPath('Frontend/JS/Vue'))
