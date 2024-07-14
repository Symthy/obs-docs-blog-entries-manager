from domain.docs.value.doc_entry_id import DocEntryId
from infrastructure.documents.document_file_reader import DocumentFileReader
from infrastructure.store.blog_to_doc_entry_mapping import BlogToDocEntryMapping
from infrastructure.store.stored_entry_title_finder import StoredEntryTitleFinder


class EntryLinkValidator:
    def __init__(self, doc_entry_title_finder: StoredEntryTitleFinder,
                 blog_to_doc_mapping: BlogToDocEntryMapping, document_reader: DocumentFileReader):
        self.__entry_title_finder = doc_entry_title_finder
        self.__blog_to_doc_mapping = blog_to_doc_mapping
        self.__document_reader = document_reader

    def validate(self, doc_id: DocEntryId) -> bool:
        doc_data_set = self.__document_reader.find(doc_id)
        for title in doc_data_set.doc_content.internal_link_titles:
            doc_entry_opt = self.__entry_title_finder.find(title)
            if doc_entry_opt is None:
                return False
            blog_entry_id_opt = self.__blog_to_doc_mapping.find_blog_entry_id(doc_entry_opt.id)
            if blog_entry_id_opt is None:
                return False
        return True
