import pytest
from assertpy import assert_that

from api.api_client import ApiClient
from config.blog_config import BlogConfig
from infrastructure.hatena.api.api_client_factory import ApiClientFactory
from tests._test_data.path_resolver import resolve_test_data_dir_path


@pytest.fixture
def api_client_factory():
    data_path = resolve_test_data_dir_path()
    blog_conf = BlogConfig.load(data_path.add_file('blog.conf'))
    return ApiClientFactory(blog_conf)


def test_build_blog_api_client(api_client_factory: ApiClientFactory):
    actual: ApiClient = api_client_factory.build_blog_api_client()
    assert_that(actual.base_url).is_equal_to('https://blog.hatena.ne.jp/SYM_dummy/dummy.hatenablog.com/atom/entry/')
    assert_that(actual.base_headers).contains_key('X-WSSE')


def test_build_photo_api_client(api_client_factory: ApiClientFactory):
    actual: ApiClient = api_client_factory.build_photo_api_client()
    assert_that(actual.base_url).is_equal_to('https://f.hatena.ne.jp/atom/')
    assert_that(actual.base_headers).contains_key('X-WSSE')
