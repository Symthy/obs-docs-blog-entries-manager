from assertpy import assert_that

from blogs.domain.entity.blog_entry import BlogEntry
from blogs.domain.factory.blog_entry_deserializer import BlogEntryDeserializer
from blogs.domain.value.blog_entry_id import BlogEntryId
from docs.domain.entity.doc_entry import DocEntry
from docs.domain.factory.doc_entry_deserializer import DocEntryDeserializer
from docs.domain.value.doc_entry_id import DocEntryId
from stores.infrastructure.stored_entry_accessor import StoredEntryAccessor
from tests.stores.infrastructure._data.path_resolver import resolve_test_data_dir_path


class TestStoredEntryAccessor:

    def test_load_entry_when_blog_entry(self):
        data_path = resolve_test_data_dir_path()
        blog_data_path = data_path.add_dir('blog')
        accessor = StoredEntryAccessor[BlogEntry, BlogEntryId](blog_data_path, BlogEntryDeserializer())
        actual: BlogEntry = accessor.load_entry(BlogEntryId('13574176438055789968'))
        assert_that(actual.id.value).is_equal_to('13574176438055789968')
        assert_that(actual.pickup).is_true()
        assert_that(actual.category_path.value.value).is_equal_to('Portfolio')
        assert_that(actual.categories).is_length(2)
        assert_that(actual.images.items).is_length(2)

    def test_load_entry_when_doc_entry(self):
        data_path = resolve_test_data_dir_path()
        doc_data_path = data_path.add_dir('doc')
        accessor = StoredEntryAccessor[DocEntry, DocEntryId](doc_data_path, DocEntryDeserializer())
        actual: DocEntry = accessor.load_entry(DocEntryId('20220123190520'))
        assert_that(actual.id.value).is_equal_to('20220123190520')
        assert_that(actual.pickup).is_false()
        assert_that(actual.category_path.value.value).is_equal_to('Portfolio')
        assert_that(actual.categories).is_length(2)
