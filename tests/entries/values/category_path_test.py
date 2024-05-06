from domain.entries.values.category_path import CategoryPath


def test_is_child():
    child = CategoryPath('Backend/DB/SQL')
    parent = CategoryPath('Backend/DB')
    assert parent.is_child(child)


def test_hash():
    category_path_to_dummy = {
        CategoryPath('Backend/DB/SQL'): '1',
        CategoryPath('Backend/DB'): '2',
        CategoryPath('Frontend/JS/React'): '3',
        CategoryPath('Frontend/JS'): '4'
    }

    category_path_to_dummy.pop(CategoryPath('Backend/DB/SQL'))
    assert len(category_path_to_dummy) == 3
    assert category_path_to_dummy[CategoryPath('Frontend/JS/React')] == '3'
