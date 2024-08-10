from assertpy import assert_that

from domain.blogs.value.blog_entry_id import BlogEntryId
from domain.docs.value.doc_entry_id import DocEntryId
from files import file_system
from infrastructure.store.blog_to_doc_entry_mapping import BlogToDocEntryMapping
from tests.infrastructure.store._data.path_resolver import resolve_test_data_dir_path


class TestBlogToDocEntryMapping:
    def setup_method(self):
        data_path = resolve_test_data_dir_path()
        self.__mapping = BlogToDocEntryMapping(file_system.join_path(data_path, 'blog_to_doc_mapping.json'))

    def test_find_doc_entry_id(self):
        doc_entry_id = self.__mapping.find_doc_entry_id(BlogEntryId('13574176438059028795'))
        assert_that(doc_entry_id.value).is_equal_to('20220201211144')

    def test_find_blog_entry_id(self):
        blog_entry_id = self.__mapping.find_blog_entry_id(DocEntryId('20220201211144'))
        assert_that(blog_entry_id.value).is_equal_to('13574176438059028795')

    def test_find_blog_entry_ids(self):
        doc_ids = [DocEntryId('20220123190520'), DocEntryId('20220123193352'), DocEntryId('20220123193618'),
                   DocEntryId('20220123193918'), DocEntryId('20220129233432')]
        blog_entry_ids = self.__mapping.find_blog_entry_ids(doc_ids)
        assert_that(blog_entry_ids).extracting('value').contains_only('13574176438055789968', '13574176438055793556',
                                                                      '13574176438055794328', '13574176438055795579',
                                                                      '13574176438058009696')
