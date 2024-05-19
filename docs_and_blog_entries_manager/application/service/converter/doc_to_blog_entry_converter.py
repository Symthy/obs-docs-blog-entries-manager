from common.constants import BLOG_CATEGORY
from domain.blogs.datasource.model.post_blog_entry import PostBlogEntry
from domain.docs.datasources.model.document_dataset import DocumentDataset


class DocToBlogEntryConverter:

    @classmethod
    def convert_to_post(cls, doc_dataset: DocumentDataset) -> PostBlogEntry:
        title = doc_dataset.doc_entry.title
        category_path = doc_dataset.doc_entry.category_path
        categories = [category for category in doc_dataset.doc_entry.categories if category != BLOG_CATEGORY]
        return PostBlogEntry(title, doc_dataset.doc_content.value, category_path, categories,
                             doc_dataset.doc_content.image_paths)

    # def __init__(self, blog_to_doc_entry_mapping: BlogToDocEntryMapping,
    #              stored_blog_entries_accessor: StoredBlogEntriesAccessor):
    #     self.__blog_to_doc_entry_mapping = blog_to_doc_entry_mapping
    #     self.__stored_blog_entries_accessor = stored_blog_entries_accessor
    #
    # def convert(self, doc_entry: DocEntry) -> BlogEntry:
    #     blog_id: Optional[BlogEntryId] = self.__blog_to_doc_entry_mapping.find_blog_entry_id(doc_entry.id)
    #     if blog_id is None:
    #         builder = BlogEntryBuilder()
    #         builder.title(doc_entry.title)
    #         builder.updated_at(doc_entry.updated_at)
    #         builder.category_path(doc_entry.category_path)
    #         builder.categories([category for category in doc_entry.categories if category != BLOG_CATEGORY])
    #         # Todo: 画像
    #         # builder.doc_images(doc_entry.)
    #         return builder.build()
    #
    #     existed_blog_entry: BlogEntry = self.__stored_blog_entries_accessor.load_entry(blog_id)
    #     if doc_entry.updated_at.is_time_after(existed_blog_entry.updated_at):
    #         builder = BlogEntryBuilder(existed_blog_entry)
    #         builder.title(doc_entry.title)
    #         builder.updated_at(doc_entry.updated_at)
    #         builder.category_path(doc_entry.category_path)
    #         builder.categories([category for category in doc_entry.categories if category != BLOG_CATEGORY])
    #         # Todo: 画像
    #         # builder.doc_images(doc_entry.)
    #         return builder.build()
    #     return existed_blog_entry
