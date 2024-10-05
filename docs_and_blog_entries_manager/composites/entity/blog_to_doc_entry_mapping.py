from typing import Optional

from blogs.domain.value import BlogEntryId
from common.constants import LOCAL_STORE_DIR_PATH
from docs.domain.value import DocEntryId
from files import json_file
from files.value import FilePath


# Todo: ファイル読み込み処理分離
class BlogToDocEntryMapping:
    __HATENA_BLOG_TO_DOC_ENTRY_FILE = 'blog_to_doc_mapping.json'  # rename from hatena_blog_to_doc_dict.json
    __HATENA_BLOG_TO_DOC_ENTRY_PATH = FilePath(LOCAL_STORE_DIR_PATH + __HATENA_BLOG_TO_DOC_ENTRY_FILE)

    def __init__(self, stored_json_file_path: FilePath = None):
        file_path = self.__HATENA_BLOG_TO_DOC_ENTRY_PATH if stored_json_file_path is None else stored_json_file_path
        blog_to_docs: dict[str, str] = json_file.load(file_path)
        self.__blog_id_to_doc_id: dict[BlogEntryId, DocEntryId] = {BlogEntryId(b): DocEntryId(d) for b, d in
                                                                   blog_to_docs.items()}
        self.__doc_id_to_blog_id: dict[DocEntryId, BlogEntryId] = {}
        for blog_entry_id, doc_entry_id in self.__blog_id_to_doc_id.items():
            self.__doc_id_to_blog_id[doc_entry_id] = blog_entry_id

    def find_blog_entry_id(self, doc_entry_id: DocEntryId) -> Optional[BlogEntryId]:
        if doc_entry_id in self.__doc_id_to_blog_id:
            return self.__doc_id_to_blog_id[doc_entry_id]
        return None

    def find_blog_entry_ids(self, doc_entry_ids: list[DocEntryId]) -> list[BlogEntryId]:
        blog_entry_ids = []
        for doc_entry_id in doc_entry_ids:
            blog_entry_id_opt = self.find_blog_entry_id(doc_entry_id)
            if blog_entry_id_opt is None:
                continue
            blog_entry_ids.append(blog_entry_id_opt)
        return blog_entry_ids

    def find_doc_entry_id(self, blog_entry_id: BlogEntryId) -> Optional[DocEntryId]:
        if self.exist(blog_entry_id):
            return self.__blog_id_to_doc_id[blog_entry_id]
        return None

    def find_all(self) -> dict[BlogEntryId, DocEntryId]:
        return self.__blog_id_to_doc_id

    def exist(self, blog_entry_id: BlogEntryId) -> bool:
        return blog_entry_id in self.__blog_id_to_doc_id

    def push_entry_pair(self, blog_entry_id: BlogEntryId, doc_entry_id: DocEntryId):
        self.__blog_id_to_doc_id[blog_entry_id] = doc_entry_id
        self.__doc_id_to_blog_id[doc_entry_id] = blog_entry_id

    def save(self):
        json_file.save(self.__HATENA_BLOG_TO_DOC_ENTRY_PATH, self.__blog_id_to_doc_id)
