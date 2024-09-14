from config.blog_config import BlogConfig
from tests._test_data.path_resolver import resolve_test_data_dir_path


def test_load():
    data_path = resolve_test_data_dir_path()
    blog_conf = BlogConfig.load(data_path.add_file('blog.conf'))
    assert blog_conf.hatena_id == 'SYM_dummy'
    assert blog_conf.blog_id == 'dummy.hatenablog.com'
    assert blog_conf.api_key == 'dummy_key'
    assert blog_conf.summary_entry_id == '13574176438055689423'
    assert blog_conf.summary_entry_title == 'Knowledge＆Index（全記事一覧）'
