from datetime import datetime

from assertpy import assert_that

from application.service.converter.blog_to_doc_content_converter import BlogToDocContentConverter
from domain.blogs.datasource.model.posted_blog_entry import PostedBlogEntry
from domain.blogs.value.blog_entry_id import BlogEntryId
from files.file_system import join_path
from infrastructure.store.blog_to_doc_entry_mapping import BlogToDocEntryMapping
from infrastructure.store.factory.stored_entries_accessor_factory import StoredEntriesAccessorFactory
from infrastructure.store.stored_entry_title_finder import StoredEntryTitleFinder
from tests.application.service.converter._data.path_resolver import resolve_test_data_dir_path


class TestBlogToDocContentConverter:
    def setup_method(self):
        dir_path = resolve_test_data_dir_path()
        store_dir = join_path(dir_path, 'store')
        docs_dir = join_path(dir_path, 'docs')
        blog_to_doc_mapping = BlogToDocEntryMapping(join_path(store_dir, 'blog_to_doc_mapping.json'))
        stored_doc_entries_accessor = StoredEntriesAccessorFactory(store_dir).build_for_doc()
        stored_blog_entries_accessor = StoredEntriesAccessorFactory(store_dir).build_for_blog()
        blog_entry_title_finder = StoredEntryTitleFinder(stored_blog_entries_accessor)
        self.__converter = BlogToDocContentConverter('symthy.hatenablog.com', blog_entry_title_finder,
                                                     blog_to_doc_mapping, stored_doc_entries_accessor)

    def test_convert(self):
        content = """
## Test Blog Entry 

テスト用のドキュメント

リンク１: [test_entry_2](https://symthy.hatenablog.com/entry/2024/07/20/120001)

リンク２: [test_entry_3](https://symthy.hatenablog.com/entry/2024/07/20/120002)

aaa bbb

"""

        blog_entry = PostedBlogEntry(
            'SYM_simu', BlogEntryId('13574176438055799999'), 'dummy_title', content,
            'https://symthy.hatenablog.com/entry/2024/07/20/120001', datetime.now(), ['Others', 'test'])
        doc_content = self.__converter.convert(blog_entry, 'Others', {})
        assert_that(doc_content).is_not_none()
        assert_that(doc_content.value).is_equal_to("""
## Test Blog Entry 

テスト用のドキュメント

リンク１: [[test_entry_2]]

リンク２: [[test_entry_3]]

aaa bbb

#Others #test
""")
