import re
from typing import List

from blogs.domain.entity import PhotoEntries


def join_lines(lines: List[str]) -> str:
    data = ''
    for line in lines:
        data = data + line + '\n'
    return data


# Todo: 置き場所検討
def replace_image_link_in_md_data(md_file_data: str, photo_entries: PhotoEntries) -> str:
    replaced_data = md_file_data
    for image_filename in photo_entries.image_filenames:
        image_match_regex = r"!\[.*\]\(.*" + re.escape(image_filename) + r'.*\)'
        replaced_data = re.sub(image_match_regex, f'[{photo_entries.get_syntax(image_filename)}]', replaced_data)
        print(f'[Info] Success: replace image link in md file data (image: {image_filename})')
    return replaced_data
