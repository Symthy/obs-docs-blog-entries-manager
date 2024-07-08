from typing import List

from application.service.converter.blog_to_doc_entry_converter import BlogToDocEntryConverter
from application.service.converter.photo_entries_to_doc_images_converter import PhotoEntriesToDocImagesConverter
from domain.blogs.datasource.interface import IBlogEntryRepository
from domain.blogs.datasource.model.posted_blog_entry import PostedBlogEntry
from domain.docs.entity.doc_entry import DocEntry
from domain.docs.value.doc_content import DocContent
from domain.docs.value.doc_entry_id import DocEntryId
from infrastructure.documents.document_file_accessor import DocumentFileAccessor
from infrastructure.store.composite.stored_both_entries_accessor import StoredBothEntriesAccessor


class EntryCollectorService:
    """
    blogから投稿済み記事を収集し、ローカルに保存する
    """

    def __init__(self,
                 posted_blog_entry_repository: IBlogEntryRepository,
                 blog_to_doc_entry_converter: BlogToDocEntryConverter,
                 photo_entries_to_doc_images_converter: PhotoEntriesToDocImagesConverter,
                 stored_both_entries_accessor: StoredBothEntriesAccessor,
                 document_file_accessor: DocumentFileAccessor):
        self.__posted_blog_entry_repository = posted_blog_entry_repository
        self.__blog_to_doc_entry_converter = blog_to_doc_entry_converter
        self.__photo_entries_to_doc_images_converter = photo_entries_to_doc_images_converter
        self.__stored_both_entries_accessor = stored_both_entries_accessor
        self.__document_file_accessor = document_file_accessor

    def execute(self):
        posted_blog_entries: List[PostedBlogEntry] = self.__posted_blog_entry_repository.find_all()
        self.__save_all(posted_blog_entries)

    def __save_all(self, posted_blog_entries: List[PostedBlogEntry]):
        # Todo: errorケース md保存成功して、json保存失敗したら、mdは残す（他機能で救えるため
        for posted_blog_entry in posted_blog_entries:
            doc_entry_id = self.__save_document(posted_blog_entry)
            blog_entry = posted_blog_entry.convert_to_blog_entry()
            doc_entry: DocEntry = self.__blog_to_doc_entry_converter.convert(blog_entry, doc_entry_id)
            self.__stored_both_entries_accessor.save_entry(blog_entry, doc_entry)

    def __save_document(self, posted_blog_entry: PostedBlogEntry) -> DocEntryId:
        doc_entry_path = posted_blog_entry.category_path.value
        doc_content = DocContent(posted_blog_entry.content.value_with_inserted_categories, doc_entry_path)
        doc_images = self.__photo_entries_to_doc_images_converter.execute(posted_blog_entry.photo_entries,
                                                                          doc_entry_path)
        doc_entry_id = self.__document_file_accessor.save(doc_entry_path, posted_blog_entry.title,
                                                          doc_content, doc_images)
        return doc_entry_id

    def __replace_entry_links(self):
        # Todo: 最後に、記事へのリンクをまとめて置換する
        pass
