import codecs

from docs_and_blog_entries_manager.logs.logger import Logger
from files.value.file_path import FilePath


def read_lines(file_path: FilePath) -> list[str]:
    try:
        with codecs.open(file_path.value, mode='r', encoding='utf-8') as f:
            lines = f.readlines()
            lines_exclusion_empty = list(
                filter(lambda line: line.replace(' ', '').replace('\r', '').replace('\n', '') != '', lines))
            lines_exclusion_comment = list(filter(lambda line: not line.startswith('#'), lines_exclusion_empty))
            return [line.replace('\r', '').replace('\n', '') for line in lines_exclusion_comment]
    except Exception as e:
        Logger.warn(f'read failed {file_path}: {e}')
        return []
