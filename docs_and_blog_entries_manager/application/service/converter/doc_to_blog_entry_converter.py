from common.constants import BLOG_CATEGORY
from domain.blogs.datasource.model.not_posted_blog_entry import PrePostBlogEntry
from domain.docs.datasources.model.document_dataset import DocumentDataset


class DocToBlogEntryConverter:

    @classmethod
    def convert_to_prepost(cls, doc_dataset: DocumentDataset) -> PrePostBlogEntry:
        title = doc_dataset.doc_entry.title
        category_path = doc_dataset.doc_entry.category_path
        categories = [category for category in doc_dataset.doc_entry.categories if category != BLOG_CATEGORY]
        return PrePostBlogEntry(title, doc_dataset.doc_content.value, category_path, categories,
                                doc_dataset.doc_content.image_paths)
