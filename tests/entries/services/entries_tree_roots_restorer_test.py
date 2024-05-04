import pytest

from entries.entity.entries_tree_roots import EntriesTreeRoots
from entries.interface import IEntries
from entries.services.entries_tree_roots_restorer import EntriesTreeRootsRestorer
from entries.values.category_path import CategoryPath
from store.datasources.stored_entries_accessor import StoredEntriesAccessor
from store.entity.category_tree_definition import CategoryTreeDefinition


@pytest.fixture
def category_tree_definition(mocker) -> CategoryTreeDefinition:
    mock_category_tree_def = mocker.Mock(spec=CategoryTreeDefinition)
    mock_category_tree_def.category_full_paths = [
        CategoryPath('Backend/DB/SQL'),
        CategoryPath('Frontend/JS/React'),
        CategoryPath('Frontend/JS/React/Next'),
        CategoryPath('Frontend/JS/Vue'),
    ]
    return mock_category_tree_def


@pytest.fixture
def input_mocks(mocker):
    mock_entries0 = mocker.Mock(spec=IEntries)
    mock_entries1 = mocker.Mock(spec=IEntries)
    mock_entries2 = mocker.Mock(spec=IEntries)
    mock_entries3 = mocker.Mock(spec=IEntries)
    mock_entries4 = mocker.Mock(spec=IEntries)
    mock_entries5 = mocker.Mock(spec=IEntries)
    mock_entries6 = mocker.Mock(spec=IEntries)
    mock_entries7 = mocker.Mock(spec=IEntries)

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


def test_build_all_category_path_to_entries(input_mocks):
    restorer = EntriesTreeRootsRestorer(
        input_mocks[CategoryTreeDefinition.__name__],
        input_mocks[StoredEntriesAccessor.__name__])
    actual = restorer.build_all_category_path_to_entries_for_testing()
    assert actual.get(CategoryPath('Backend/DB/SQL')) == input_mocks['mock_entries'][0]
    assert actual.get(CategoryPath('Backend/DB')) == input_mocks['mock_entries'][1]
    assert actual.get(CategoryPath('Backend')) == input_mocks['mock_entries'][2]
    assert actual.get(CategoryPath('Frontend/JS/React/Next')) == input_mocks['mock_entries'][3]
    assert actual.get(CategoryPath('Frontend/JS/React')) == input_mocks['mock_entries'][4]
    assert actual.get(CategoryPath('Frontend/JS/Vue')) == input_mocks['mock_entries'][5]
    assert actual.get(CategoryPath('Frontend/JS')) == input_mocks['mock_entries'][6]
    assert actual.get(CategoryPath('Frontend')) == input_mocks['mock_entries'][7]


def test_execute(input_mocks):
    restorer = EntriesTreeRootsRestorer(
        input_mocks[CategoryTreeDefinition.__name__],
        input_mocks[StoredEntriesAccessor.__name__])
    actual: EntriesTreeRoots = restorer.execute()

    assert actual.root_num() == 2
    assert actual.get_top_tree(CategoryPath('Backend')).entries == input_mocks['mock_entries'][2]
    assert actual.get_top_tree(CategoryPath('Frontend')).entries == input_mocks['mock_entries'][7]
    assert len(actual.search_tree(CategoryPath('Frontend/JS')).children) == 2
    assert CategoryPath('Frontend/JS/React') in actual.search_tree(CategoryPath('Frontend/JS')).child_category_paths
    assert CategoryPath('Frontend/JS/Vue') in actual.search_tree(CategoryPath('Frontend/JS')).child_category_paths


if __name__ == '__main__':
    pytest.main()
