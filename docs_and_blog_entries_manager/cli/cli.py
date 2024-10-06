from blogs.infrastructure.factory import BlogPhotoEntryRepositoryFactory, StoredBlogEntriesAccessorFactory
from blogs.infrastructure.image import ImageDownLoader
from blogs.usecase import BlogEntrySaverService
from cli.comand.blog.blog_command import BlogCommand
from cli.comand.blog.options.collect_blog_entry_option import CollectBlogEntryOption
from cli.comand.blog.options.display_blog_entry_option import DisplayBlogEntryOption
from cli.comand.blog.options.push_all_blog_entry_option import PushAllBlogEntryOption
from cli.comand.blog.options.push_blog_entry_option import PushBlogEntryOption
from cli.comand.doc import DocCommand
from cli.comand.doc.options.import_document_option import ImportDocumentOption
from cli.comand.doc.options.push_all_document_option import PushAllDocumentOption
from cli.comand.doc.options.push_document_option import PushDocumentOption
from cli.comand.main_command import MainCommand
from composites.converter import BlogToDocEntryConverter, BlogPhotosToDocImagesConverter, BlogToDocContentConverter, \
    DocToBlogEntryConverter
from composites.entity import BlogToDocEntryMapping
from composites.usecase import BlogEntryAllUpdaterService, EntryToBlogPusherService, BlogEntryRemoverService
from composites.usecase.collector import BlogEntryCollectorService
from composites.usecase.collector.collected_entry_registerer import CollectedEntryRegisterer
from composites.usecase.collector.collected_entry_updater import CollectedEntryUpdater
from composites.usecase.collector.entry_document_saver import EntryDocumentSaver
from config.blog_config import BlogConfig
from docs.infrastructure import DocumentFileMover, DocumentFileReader
from docs.infrastructure.factory import DocumentFileAccessorFactory, StoredDocEntriesAccessorFactory, \
    StoredDocEntryListDeserializer
from docs.infrastructure.file import AllDocumentPathResolver
from docs.infrastructure.work import WorkingDocumentFileAccessor
from docs.usecase import LocalDocImporterService, LocalDocOrganizerService, LocalDocPusherService
from docs.usecase.validator import DocEntryLinkValidator
from entries.domain.entity import CategoryTreeDefinition
from stores.infrastructure import StoredEntryTitleFinder


def main():
    # Todo: factory設けるかDIライブラリ入れるか検討要
    blog_config = BlogConfig.load()
    blog_to_doc_mapping = BlogToDocEntryMapping()
    stored_doc_entry_list = StoredDocEntryListDeserializer().deserialize()
    stored_doc_entry_accessor = StoredDocEntriesAccessorFactory().build(stored_doc_entry_list)
    stored_blog_entry_accessor = StoredBlogEntriesAccessorFactory().build()
    category_tree_def = CategoryTreeDefinition.build()
    blog_repository = BlogPhotoEntryRepositoryFactory(blog_config).build()
    document_file_accessor = DocumentFileAccessorFactory(
        stored_doc_entry_accessor, stored_doc_entry_list, category_tree_def).build()
    blog_entry_repository = BlogPhotoEntryRepositoryFactory(blog_config).build()
    blog_entry_title_finder = StoredEntryTitleFinder(stored_blog_entry_accessor)
    doc_entry_title_finder = StoredEntryTitleFinder(stored_doc_entry_accessor)
    document_file_reader = DocumentFileReader(
        stored_doc_entry_accessor, stored_doc_entry_list, AllDocumentPathResolver(category_tree_def))
    document_file_mover = DocumentFileMover(document_file_reader, stored_doc_entry_accessor)
    image_downloader = ImageDownLoader()
    blog_photo_to_doc_images_converter = BlogPhotosToDocImagesConverter(image_downloader)
    blog_to_doc_content_converter = BlogToDocContentConverter(
        blog_config.blog_id, blog_entry_title_finder, blog_to_doc_mapping, stored_doc_entry_accessor)
    blog_to_doc_entry_converter = BlogToDocEntryConverter(
        blog_to_doc_mapping, stored_doc_entry_accessor, blog_photo_to_doc_images_converter,
        blog_to_doc_content_converter)
    doc_to_blog_entry_converter = DocToBlogEntryConverter(doc_entry_title_finder, blog_to_doc_mapping,
                                                          stored_blog_entry_accessor)

    entry_document_saver = EntryDocumentSaver(
        blog_to_doc_mapping, stored_blog_entry_accessor, stored_doc_entry_accessor, document_file_accessor,
        blog_to_doc_entry_converter)
    collected_entry_register = CollectedEntryRegisterer(
        blog_photo_to_doc_images_converter, blog_to_doc_content_converter, entry_document_saver, document_file_accessor)
    collected_entry_updater = CollectedEntryUpdater(
        blog_photo_to_doc_images_converter, blog_to_doc_content_converter, entry_document_saver, document_file_mover)
    entry_collector_service = BlogEntryCollectorService(
        blog_to_doc_mapping, blog_entry_repository, collected_entry_register, collected_entry_updater)
    blog_entry_saver_service = BlogEntrySaverService(blog_repository, stored_blog_entry_accessor)
    doc_entry_link_validator = DocEntryLinkValidator(doc_entry_title_finder, blog_to_doc_mapping, document_file_reader)
    entry_to_blog_pusher_service = EntryToBlogPusherService(
        document_file_accessor, doc_to_blog_entry_converter, blog_to_doc_mapping, doc_entry_link_validator,
        blog_entry_saver_service, stored_blog_entry_accessor)
    blog_entry_remover_service = BlogEntryRemoverService(
        document_file_accessor, blog_repository, blog_to_doc_mapping, stored_blog_entry_accessor)
    blog_entry_all_updater_service = BlogEntryAllUpdaterService(
        stored_doc_entry_accessor, stored_blog_entry_accessor, entry_to_blog_pusher_service, blog_entry_remover_service,
        blog_to_doc_mapping, document_file_reader)

    working_doc_file_accessor = WorkingDocumentFileAccessor(stored_doc_entry_accessor, document_file_mover)
    local_doc_importer_service = LocalDocImporterService(document_file_accessor, stored_doc_entry_accessor)
    local_doc_organizer_service = LocalDocOrganizerService(
        category_tree_def, document_file_mover, document_file_reader, stored_doc_entry_accessor)
    local_doc_pusher_service = LocalDocPusherService(working_doc_file_accessor, document_file_mover)
    MainCommand(
        BlogCommand(blog_config,
                    DisplayBlogEntryOption(blog_config),
                    CollectBlogEntryOption(entry_collector_service),
                    PushAllBlogEntryOption(blog_entry_all_updater_service),
                    PushBlogEntryOption(entry_to_blog_pusher_service)),
        DocCommand(blog_config,
                   ImportDocumentOption(local_doc_importer_service, local_doc_organizer_service),
                   PushAllDocumentOption(local_doc_pusher_service, entry_to_blog_pusher_service),
                   PushDocumentOption(local_doc_pusher_service, entry_to_blog_pusher_service))
    ).run()


if __name__ == '__main__':
    main()
