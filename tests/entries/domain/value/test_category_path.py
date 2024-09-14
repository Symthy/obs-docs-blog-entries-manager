from entries.domain.value import CategoryPath


class TestCategoryPath:
    def test_is_child(self):
        child = CategoryPath('Backend/DB/SQL')
        parent = CategoryPath('Backend/DB')
        assert parent.is_child(child)

    def test_hash(self):
        category_path_to_dummy = {
            CategoryPath('Backend/DB/SQL'): '1',
            CategoryPath('Backend/DB'): '2',
            CategoryPath('Frontend/JS/React'): '3',
            CategoryPath('Frontend/JS'): '4'
        }

        category_path_to_dummy.pop(CategoryPath('Backend/DB/SQL'))
        assert len(category_path_to_dummy) == 3
        assert category_path_to_dummy[CategoryPath('Frontend/JS/React')] == '3'
