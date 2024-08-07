from assertpy import assert_that

from application.service.converter.doc_to_blog_entry_converter import DocToBlogEntryConverter
from domain.docs.value.doc_entry_id import DocEntryId
from domain.entries.values.category_path import CategoryPath
from files.file_system import join_path
from infrastructure.documents.document_file_reader import DocumentFileReader
from infrastructure.store.blog_to_doc_entry_mapping import BlogToDocEntryMapping
from infrastructure.store.factory.stored_entries_accessor_factory import StoredEntriesAccessorFactory
from infrastructure.store.stored_entry_title_finder import StoredEntryTitleFinder
from tests.application.service.converter._data.path_resolver import resolve_test_data_dir_path


class TestDocToBlogEntryConverter:
    def setup_method(self):
        dir_path = resolve_test_data_dir_path()
        store_dir = join_path(dir_path, 'store')
        docs_dir = join_path(dir_path, 'docs')
        blog_to_doc_mapping = BlogToDocEntryMapping(join_path(store_dir, 'blog_to_doc_mapping.json'))
        stored_doc_entries_accessor = StoredEntriesAccessorFactory(store_dir).build_for_doc()
        stored_blog_entries_accessor = StoredEntriesAccessorFactory(store_dir).build_for_blog()
        doc_entry_title_finder = StoredEntryTitleFinder(stored_doc_entries_accessor)
        self.__converter = DocToBlogEntryConverter(doc_entry_title_finder, blog_to_doc_mapping,
                                                   stored_blog_entries_accessor)
        self.__document_reader = DocumentFileReader(docs_dir, stored_doc_entries_accessor)

    def test_convert_to_prepost(self):
        expected_content = """## Test Document

テスト用のドキュメント

[test_entry_2](https://dummy.hatenablog.com/entry/2024/07/20/120001)

aaa

[test_entry_3](https://dummy.hatenablog.com/entry/2024/07/20/120002)

bbb
#Others
"""

        doc_dataset = self.__document_reader.find(DocEntryId('20240720120000111111'))
        pre_post_entry = self.__converter.convert_to_prepost(doc_dataset)
        assert_that(pre_post_entry.title).is_equal_to('test_entry_1')
        assert_that(pre_post_entry.category_path).is_equal_to(CategoryPath('Others'))
        assert_that(pre_post_entry.categories).contains_only('test')
        assert_that(pre_post_entry.content).is_equal_to(expected_content)
