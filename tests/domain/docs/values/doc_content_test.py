import pytest
from assertpy import assert_that

from domain.docs.value.doc_content import DocContent
from domain.entries.values.category_path import CategoryPath

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


def test_doc_content():
    doc_content = DocContent(CONTENT_FOR_TESTING, 'dummy')
    assert_that(doc_content.category_path).is_equal_to(CategoryPath('Github/GithubActions/README'))
    assert_that(doc_content.categories).contains_only('dummy', 'profile')
    assert_that(doc_content.image_paths).contains_only('Github/GithubActions/README/images/github-profile-summary.png')
    assert_that(doc_content.internal_link_titles).contains_only('Github Actions')
    content_with_removed_category = DocContent(doc_content.value_with_removed_categories, 'dummy')
    assert_that(content_with_removed_category.category_path).is_equal_to(CategoryPath.non_category())


@pytest.mark.parametrize("content, expected", [
    ('\n#dummy\n', '\n'),
    ('\n#test/dummy #category\n', '\n'),
    ('\n #test/dummy #category\n', '\n'),
    ('\n #test/dummy #category \n', '\n'),
    ('\n#test/dummy #category1, #category2\n', '\n')
])
def test_value_with_removed_categories(content, expected):
    content = '\n #test/dummy #category \n'
    doc_content = DocContent(content, 'dummy')
    print(doc_content.value_with_removed_categories)
    assert_that(doc_content.value_with_removed_categories).is_equal_to(expected)
