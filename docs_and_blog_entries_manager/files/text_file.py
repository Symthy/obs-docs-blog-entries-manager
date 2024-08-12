import codecs

from docs_and_blog_entries_manager.logs.logger import Logger
from files.value.file_path import FilePath


def read_file(file_path: FilePath) -> str:
    with codecs.open(file_path.value, mode='r', encoding='utf-8') as f:
        lines = f.read()
    return lines


def read_first_line(file_path: FilePath) -> str:
    with codecs.open(file_path.value, mode='r', encoding='utf-8') as f:
        line = f.readline()
    return line.lstrip('#').strip()


def write_file(file_path: FilePath, text: str):
    try:
        with codecs.open(file_path.value, mode='w', encoding='utf-8') as f:
            f.write(text)
    except Exception as e:
        Logger.warn(f'write failed {file_path}: {e}')


def write_line(file_path: FilePath, line: str):
    write_file(file_path, line)


def write_lines(file_path: FilePath, lines: list[str]):
    write_file(file_path, '\n'.join(lines))


def add_end_line(file_path: FilePath, line: str):
    with open(file_path.value, mode='a') as f:
        f.write(f'{line}\n')
