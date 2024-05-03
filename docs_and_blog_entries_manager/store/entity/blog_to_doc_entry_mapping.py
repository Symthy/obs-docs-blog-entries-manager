from typing import Dict, Optional, List

from common.constants import LOCAL_STORAGE_DIR_PATH
from files import json_file


class BlogToDocEntryMapping:
    __HATENA_BLOG_TO_DOC_ENTRY_FILE = 'blog_to_doc_mapping.json'  # rename from hatena_blog_to_doc_dict.json
    __HATENA_BLOG_TO_DOC_ENTRY_PATH = LOCAL_STORAGE_DIR_PATH + __HATENA_BLOG_TO_DOC_ENTRY_FILE

    def __init__(self):
        blog_to_doc: Dict[str, str] = json_file.load(self.__HATENA_BLOG_TO_DOC_ENTRY_PATH)
        self.__blog_id_to_doc_id: Dict[str, str] = blog_to_doc
        self.__doc_id_to_blog_id: Dict[str, str] = {}
        for blog_entry_id, doc_entry_id in blog_to_doc.items():
            self.__doc_id_to_blog_id[doc_entry_id] = blog_entry_id

    def find_blog_entry_id(self, doc_entry_id: str) -> Optional[str]:
        if doc_entry_id in self.__doc_id_to_blog_id:
            return self.__doc_id_to_blog_id[doc_entry_id]
        return None

    def find_blog_entry_ids(self, doc_entry_ids: List[str]) -> List[str]:
        blog_entry_ids = []
        for doc_entry_id in doc_entry_ids:
            blog_entry_id_opt = self.find_blog_entry_id(doc_entry_id)
            if blog_entry_id_opt is None:
                continue
            blog_entry_ids.append(blog_entry_id_opt)
        return blog_entry_ids

    def find_doc_entry_id(self, blog_entry_id: str) -> Optional[str]:
        if blog_entry_id in self.__blog_id_to_doc_id:
            return self.__blog_id_to_doc_id[blog_entry_id]
        return None

    def push_entry_pair(self, blog_entry_id: str, doc_entry_id: str):
        self.__blog_id_to_doc_id[blog_entry_id] = doc_entry_id
        self.__doc_id_to_blog_id[doc_entry_id] = blog_entry_id

    def save(self):
        json_file.save(self.__HATENA_BLOG_TO_DOC_ENTRY_PATH, self.__blog_id_to_doc_id)
