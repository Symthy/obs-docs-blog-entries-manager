from blogs.infrastructure.factory import BlogPhotoEntryRepositoryFactory
from cli.comand.blog.blog_command import BlogCommand
from cli.comand.blog.options.collect_blog_entry_option import CollectBlogEntryOption
from cli.comand.blog.options.display_blog_entry_option import DisplayBlogEntryOption
from cli.comand.main_command import MainCommand
from composites.entity import BlogToDocEntryMapping
from composites.usecase.collector import BlogEntryCollectorService
from config.blog_config import BlogConfig
from docs.infrastructure.factory import DocumentFileAccessorFactory
from stores.factory import StoredEntriesAccessorFactory


def main():
    blog_config = BlogConfig.load()
    blog_to_doc_mapping = BlogToDocEntryMapping()
    stored_entry_accessor_factory = StoredEntriesAccessorFactory()
    stored_doc_entry_accessor = stored_entry_accessor_factory.build_for_doc()
    stored_blog_entry_accessor = stored_entry_accessor_factory.build_for_blog()
    blog_repository = BlogPhotoEntryRepositoryFactory(blog_config).build()
    doc_accessor = DocumentFileAccessorFactory(stored_doc_entry_accessor, )
    entry_collector_service = BlogEntryCollectorService()
    MainCommand(
        BlogCommand(blog_config,
                    DisplayBlogEntryOption(blog_config),
                    CollectBlogEntryOption()
                    )
    ).run()


if __name__ == '__main__':
    main()
