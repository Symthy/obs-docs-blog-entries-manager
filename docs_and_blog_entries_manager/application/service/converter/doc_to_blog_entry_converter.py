from common.constants import BLOG_CATEGORY
from domain.blogs.datasource.interface import StoredBlogEntriesAccessor
from domain.blogs.datasource.model.pre_post_blog_entry import PrePostBlogEntry
from domain.docs.datasource.model.document_dataset import DocumentDataset
from domain.docs.entity.doc_entry import DocEntry
from domain.docs.value.doc_content import DocContent
from domain.mappings.blog_to_doc_entry_mapping import BlogToDocEntryMapping
from infrastructure.store.stored_entry_title_finder import StoredEntryTitleFinder


class DocToBlogEntryConverter:
    def __init__(self, doc_entry_title_finder: StoredEntryTitleFinder[DocEntry],
                 blog_to_doc_mapping: BlogToDocEntryMapping,
                 stored_blog_entries_accessor: StoredBlogEntriesAccessor):
        self.__doc_entry_title_finder = doc_entry_title_finder
        self.__blog_to_doc_mapping = blog_to_doc_mapping
        self.__stored_blog_entries_accessor = stored_blog_entries_accessor

    def convert_to_prepost(self, doc_dataset: DocumentDataset) -> PrePostBlogEntry:
        title = doc_dataset.doc_entry.title
        category_path = doc_dataset.doc_entry.category_path
        categories = [category for category in doc_dataset.doc_entry.categories if category != BLOG_CATEGORY]
        return PrePostBlogEntry(title, self.__replace_internal_links(doc_dataset.doc_content), category_path,
                                categories, doc_dataset.doc_content.image_paths)

    def __replace_internal_links(self, content: DocContent) -> str:
        title_to_blog_entry_url: dict[str, str] = {}
        for title in content.internal_link_titles:
            linked_doc_entry = self.__doc_entry_title_finder.find(title)
            linked_blog_entry_id = self.__blog_to_doc_mapping.find_blog_entry_id(linked_doc_entry.id)
            linked_blog_entry = self.__stored_blog_entries_accessor.load_entry(linked_blog_entry_id)
            title_to_blog_entry_url[title] = linked_blog_entry.page_url
        return content.replace_internal_link_titles(title_to_blog_entry_url)
