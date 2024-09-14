from blogs.domain.datasource.interface import StoredBlogEntriesAccessor
from blogs.domain.entity import PrePostBlogEntry
from common.constants import BLOG_CATEGORY
from composites.entity import BlogToDocEntryMapping
from docs.domain.entity import DocEntry, DocumentDataset
from docs.domain.value import DocContent
from stores.infrastructure import StoredEntryTitleFinder


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
