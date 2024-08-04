from __future__ import annotations

import copy
import re
from typing import List

from domain.blogs.value.blog_entry_id import BlogEntryId
from domain.blogs.value.photo_entry_id import PhotoEntryId
from domain.entries.values.category_path import CategoryPath
from logs.logger import Logger


class BlogContent:
    def __init__(self, entry_id: BlogEntryId, content: str, category_path: CategoryPath, categories: list[str],
                 hatena_id: str):
        self.__entry_id = entry_id
        self.__content = content
        self.__hatena_id = hatena_id
        self.__categories_line = f'#{category_path.value} ' + ' '.join(list(map(lambda c: f'#{c}', categories)))
        self.__photo_entry_ids: list[PhotoEntryId] = self.__extract_photo_entry_ids()

    def __extract_photo_entry_ids(self) -> list[PhotoEntryId]:
        # photo id: f:id:SYM_simu:20230101154129p:image
        photo_entry_syntax_regex = fr'\[f:id:{self.__hatena_id}:([0-9]+)p:image\]'
        photo_ids = re.findall(photo_entry_syntax_regex, self.__content)
        return list(map(lambda pid: PhotoEntryId(pid), photo_ids))

    def __rebuild(self, content) -> BlogContent:
        new_blog_content: BlogContent = copy.deepcopy(self)
        new_blog_content.__content = content
        return new_blog_content

    @property
    def id(self) -> BlogEntryId:
        return self.__entry_id

    @property
    def value(self) -> str:
        return self.__content

    @property
    def value_with_inserted_categories(self) -> BlogContent:
        # DocContent変換用。末尾にタグとして追加
        content = self.__content + '\n' + self.__categories_line + '\n'
        return self.__rebuild(content)

    @property
    def photo_entry_ids(self) -> List[PhotoEntryId]:
        return self.__photo_entry_ids

    def replace_photo_link(self, photo_entry_id: PhotoEntryId, link: str) -> BlogContent:
        if photo_entry_id in self.__photo_entry_ids:
            Logger.warn(
                f'Not exist photo entry (id: {photo_entry_id}) in blog content (blog entry id: {self.__entry_id}).')
            return self
        photo_entry_syntax = f'[f:id:{self.__hatena_id}:{photo_entry_id.value}p:image]'
        content = self.__content
        content.replace(photo_entry_syntax, link)
        return self.__rebuild(content)
