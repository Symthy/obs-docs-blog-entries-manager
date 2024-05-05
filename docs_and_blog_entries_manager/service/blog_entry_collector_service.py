from blogs.services.posted_blog_entry_collector import PostedBlogEntryCollector
from converter.service.blog_to_doc_entry_converter import BlogToDocEntryConverter


class BlogEntryCollectorService:
    def __init__(self, posted_blog_entry_collector: PostedBlogEntryCollector,
                 blog_to_doc_entry_converter: BlogToDocEntryConverter):
        self.__posted_blog_entry_collector = posted_blog_entry_collector
        self.__blog_to_doc_entry_converter = blog_to_doc_entry_converter


    def execute(self):
