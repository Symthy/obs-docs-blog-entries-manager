import pytest
from assertpy import assert_that

from docs.domain.value.doc_content import DocContent
from entries.domain.value import CategoryPath
from files.value.file_path import FilePath

CONTENT_FOR_TESTING = """
自身の Github アカウント名と同じ名前のリポジトリを作ることで、プロフィールの最初に自身の好きな内容を追加することができる

Github Actions については [[Github Actions]] を参照

以下を導入

- [GitHub Readme Stats](https://github.com/anuraghazra/github-readme-stats)

    - 作成者が公開しているアプリケーションから取得する形で実現

- [GitHub Profile Summary Cards](https://github.com/vn7n24fzkq/github-profile-summary-cards)
    - 24h に 1 回作成者が公開している　[github-profile-summary-cards](https://github.com/vn7n24fzkq/github-profile-summary-cards)
      を実行することで、自身のブランチに svg を保存/更新、それを参照する形で実現

導入することで、以下のような Summary を作ることができる

![](images/github-profile-summary.png)

テスト用データ

#Github/GithubActions/README #dummy #profile
"""


class TestDocContent:

    def test_doc_content(self):
        doc_content = DocContent(CONTENT_FOR_TESTING)
        assert_that(doc_content.category_path).is_equal_to(CategoryPath('Github/GithubActions/README'))
        assert_that(doc_content.categories).contains_only('dummy', 'profile')
        assert_that(doc_content.image_paths).contains_only(
            FilePath('Github', 'GithubActions', 'README', 'images', 'github-profile-summary.png'))
        assert_that(doc_content.internal_link_titles).contains_only('Github Actions')
        content_with_removed_category = DocContent(doc_content.value_with_removed_category_line())
        assert_that(content_with_removed_category.category_path).is_none()

    @pytest.mark.parametrize("content, expected", [
        ('\n#dummy\n', '\n'),
        ('\n#test/dummy #category\n', '\n'),
        ('\n #test/dummy #category\n', '\n'),
        ('\n #test/dummy #category \n', '\n'),
        ('\n#test/dummy #category1, #category2\n', '\n')
    ])
    def test_value_with_removed_categories(self, content, expected):
        content = '\n #test/dummy #category \n'
        doc_content = DocContent(content)
        assert_that(doc_content.value_with_removed_category_line()).is_equal_to(expected)

    def test_update_category_path(self):
        doc_content = DocContent(CONTENT_FOR_TESTING)
        actual = doc_content.update_category_path(CategoryPath('Git/Github/Actions'))
        assert_that(actual.category_path).is_equal_to(CategoryPath('Git/Github/Actions'))
        assert_that(actual.categories).contains_only('dummy', 'profile')

    def test_add_category(self):
        doc_content = DocContent(CONTENT_FOR_TESTING)
        actual = doc_content.add_category('test')
        assert_that(actual.category_path).is_equal_to(CategoryPath('Github/GithubActions/README'))
        assert_that(actual.categories).contains_only('dummy', 'profile', 'test')

    def test_remove_category(self):
        doc_content = DocContent(CONTENT_FOR_TESTING)
        actual = doc_content.remove_category('dummy')
        assert_that(actual.category_path).is_equal_to(CategoryPath('Github/GithubActions/README'))
        assert_that(actual.categories).contains_only('profile')
