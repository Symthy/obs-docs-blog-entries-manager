import re
from typing import List

from domain.blogs.value.photo_entry_id import PhotoEntryId
from domain.entries.values.category_path import CategoryPath


class BlogContent:
    def __init__(self, content: str, category_path: CategoryPath, categories: List[str], hatena_id: str):
        self.__content = content
        self.__photo_entry_ids = self.__extract_photo_entry_ids(hatena_id, content)
        self.__categories_line = f'#{category_path.value} ' + ' '.join(list(map(lambda c: f'#{c}', categories)))

    @staticmethod
    def __extract_photo_entry_ids(hatena_id: str, content: str) -> List[PhotoEntryId]:
        # photo id: f:id:SYM_simu:20230101154129p:image
        photo_entry_syntax_regex = r'\[f:id:' + hatena_id + r':([0-9]+)p:image\]'
        photo_ids = re.findall(photo_entry_syntax_regex, content)
        return list(map(lambda pid: PhotoEntryId(pid), photo_ids))

    @property
    def value(self) -> str:
        return self.__content

    @property
    def value_with_inserted_categories(self) -> str:
        # DocContent変換用。末尾にタグとして追加
        return self.__content + '\n' + self.__categories_line + '\n'

    @property
    def photo_entry_ids(self) -> List[PhotoEntryId]:
        return self.__photo_entry_ids
