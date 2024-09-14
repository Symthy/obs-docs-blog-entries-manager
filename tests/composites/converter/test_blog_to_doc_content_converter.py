from datetime import datetime

from assertpy import assert_that

from blogs.domain.entity import PostedBlogEntry
from blogs.domain.value import BlogEntryId
from composites.converter import BlogToDocContentConverter
from composites.entity import BlogToDocEntryMapping
from stores.factory import StoredEntriesAccessorFactory
from stores.infrastructure import StoredEntryTitleFinder
from tests.composites.converter._data.path_resolver import resolve_test_data_dir_path


class TestBlogToDocContentConverter:
    def setup_method(self):
        dir_path = resolve_test_data_dir_path()
        store_dir = dir_path.add_dir('store')
        docs_dir = dir_path.add_dir('docs')
        blog_to_doc_mapping = BlogToDocEntryMapping(store_dir.add_file('blog_to_doc_mapping.json'))
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
        doc_content = self.__converter.convert(blog_entry, {})
        assert_that(doc_content).is_not_none()
        assert_that(doc_content.value).is_equal_to("""
## Test Blog Entry 

テスト用のドキュメント

リンク１: [[test_entry_2]]

リンク２: [[test_entry_3]]

aaa bbb

#Others #test
""")
