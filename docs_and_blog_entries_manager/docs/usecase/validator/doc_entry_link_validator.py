from composites.entity import BlogToDocEntryMapping
from docs.domain.entity import DocEntry
from docs.domain.value import DocEntryId
from docs.infrastructure import DocumentFileReader
from stores.infrastructure import StoredEntryTitleFinder


class DocEntryLinkValidator:
    """
    指定の記事のリンク内の他記事へのリンクが存在するか(有効か)を判定
    """

    def __init__(self, doc_entry_title_finder: StoredEntryTitleFinder[DocEntry],
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
