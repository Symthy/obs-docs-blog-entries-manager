import os

import pytest
from assertpy import assert_that
from mock import mock

from api.api_client import ApiClient
from blogs.domain.entity.posted_blog_entry import PostedBlogEntry
from blogs.domain.value.blog_entry_id import BlogEntryId
from blogs.infrastructure.blog_repository import BlogRepository
from files import text_file
from files.value.file_path import FilePath


@pytest.fixture
def blog_entry_repository() -> BlogRepository:
    mock_client = mock.MagicMock(ApiClient)
    response_xml: str = text_file.read_file(
        FilePath(os.path.dirname(os.path.abspath(__file__)), '_data', 'get_response_body_data.txt'))
    mock_client.get.return_value = response_xml
    return BlogRepository(mock_client, 'dummy_hatena_id', BlogEntryId('1111111111'))


def test_find_id(blog_entry_repository):
    blog_entry: PostedBlogEntry = blog_entry_repository.find(BlogEntryId('13574176438055686757'))
    assert_that(blog_entry.title).is_equal_to('Github プロフィールのカスタマイズ')
    assert_that(blog_entry.category_path.value.value).is_equal_to('Github')
    assert_that(blog_entry.content.value).starts_with('[:contents]\n\n# Github プロフィールのカスタマイズ')
