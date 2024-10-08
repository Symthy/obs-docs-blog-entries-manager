from blogs.domain.entity import PostedBlogEntry
from composites.converter import BlogPhotosToDocImagesConverter, BlogToDocContentConverter
from docs.domain.datasource.interface import IDocumentMover
from docs.domain.entity.doc_entry import DocEntry
from logs import Logger
from .entry_document_saver import EntryDocumentSaver


class CollectedEntryUpdater:
    def __init__(self, blog_photos_to_doc_images_converter: BlogPhotosToDocImagesConverter,
                 blog_to_doc_content_converter: BlogToDocContentConverter,
                 entry_document_saver: EntryDocumentSaver, document_file_mover: IDocumentMover):
        self.__blog_photos_to_doc_images_converter = blog_photos_to_doc_images_converter
        self.__blog_to_doc_content_converter = blog_to_doc_content_converter
        self.__entry_document_saver = entry_document_saver
        self.__document_file_mover = document_file_mover

    def update(self, posted_blog_entry_to_doc_entry: dict[PostedBlogEntry, DocEntry]):
        if len(posted_blog_entry_to_doc_entry) == 0:
            return
        for posted_blog_entry, doc_entry in posted_blog_entry_to_doc_entry.items():
            if posted_blog_entry.updated_at <= doc_entry.updated_at:
                # ローカルのドキュメントの方が新しければ保存しない
                continue
            photo_entry_to_doc_image = self.__blog_photos_to_doc_images_converter.convert_to_dict(
                posted_blog_entry.photo_entries, posted_blog_entry.category_path.value)
            doc_content = self.__blog_to_doc_content_converter.convert(posted_blog_entry, photo_entry_to_doc_image)
            try:
                updated_doc_entry = self.__entry_document_saver.save(posted_blog_entry.blog_entry(), doc_content)
            except Exception as e:
                # 保存失敗の場合は可能な範囲で保存して継続
                Logger.warn(f'failed to update (title: {posted_blog_entry.title}) (detail: {e})')
                continue
            if posted_blog_entry.category_path != doc_entry.category_path:
                self.__document_file_mover.move(doc_entry.doc_file_path, updated_doc_entry.doc_file_path)
