import codecs
from typing import List

from docs_and_blog_entries_manager.logs.logger import Logger


def read_lines(file_path: str) -> str:
    with codecs.open(file_path, mode='r', encoding='utf-8') as f:
        lines = f.read()
    return lines


def read_first_line(file_path: str) -> str:
    with codecs.open(file_path, mode='r', encoding='utf-8') as f:
        line = f.readline()
    return line.lstrip('#').strip()


def __write_file(file_path, text: str):
    try:
        with codecs.open(file_path, mode='w', encoding='utf-8') as f:
            f.write(text)
    except Exception as e:
        Logger.warn(f'write failed {file_path}: {e}')


def write_line(file_path, line: str):
    __write_file(file_path, line)


def write_lines(file_path, lines: List[str]):
    __write_file(file_path, '\n'.join(lines))
