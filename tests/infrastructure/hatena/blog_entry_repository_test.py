import os

import pytest
from assertpy import assert_that
from mock import mock

from api.api_client import ApiClient
from domain.blogs.datasource.model.posted_blog_entry import PostedBlogEntry
from domain.blogs.value.blog_entry_id import BlogEntryId
from files import text_file, file_system
from infrastructure.hatena.blog_entry_repository import BlogEntryRepository


@pytest.fixture
def blog_entry_repository() -> BlogEntryRepository:
    mock_client = mock.MagicMock(ApiClient)
    response_xml: str = text_file.read_file(
        file_system.join_path(os.path.dirname(os.path.abspath(__file__)), '_data', 'get_response_body_data.txt'))
    mock_client.get.return_value = response_xml
    return BlogEntryRepository(mock_client, 'dummy_hatena_id', BlogEntryId('1111111111'))


def test_find_id(blog_entry_repository):
    blog_entry: PostedBlogEntry = blog_entry_repository.find_id(BlogEntryId('13574176438055686757'))
    assert_that(blog_entry.title).is_equal_to('Github プロフィールのカスタマイズ')
    assert_that(blog_entry.category_path.value).is_equal_to('Github')
    assert_that(blog_entry.content.value).starts_with('[:contents]\n\n# Github プロフィールのカスタマイズ')
