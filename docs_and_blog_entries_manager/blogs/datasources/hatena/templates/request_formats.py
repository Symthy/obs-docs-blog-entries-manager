from xml.sax.saxutils import escape

from common.constants import SUMMARY_PAGE_TITLE
from docs_and_blog_entries_manager.ltimes import datetime_functions


def summary_page_title() -> str:
    return __replace_xml_escape(SUMMARY_PAGE_TITLE)


__BLOG_ENTRY_TEMPLATE = """<?xml version="1.0" encoding="utf-8"?>
<entry xmlns="http://www.w3.org/2005/Atom"
       xmlns:app="http://www.w3.org/2007/app">
  <title>{title}</title>
  <author><name>{author}</name></author>
  <content type="text/x-markdown">{content}</content>
  <updated>{update_time}</updated>
  <category term="{category}" />
  <app:control>
    <app:draft>{draft}</app:draft>
  </app:control>
</entry>"""


def __replace_xml_escape(content: str) -> str:
    # entities = {
    #     '\"': '&quot;',
    #     '\'': '&apos;',
    # }
    return escape(content)  # escape: <, &, >,


def build_blog_entry_xml_body(hatena_id: str, title: str, category: str, content: str,
                              is_draft: bool = True, is_title_escape: bool = False) -> str:
    # title の escape も行わないと xml parse error が起きて投稿できない時が低確率である
    entry_xml = __BLOG_ENTRY_TEMPLATE.format(
        title=__replace_xml_escape(title) if is_title_escape else title,
        author=hatena_id,
        content=__replace_xml_escape(content),
        update_time=datetime_functions.resolve_entry_current_time(),
        category=category,
        draft='yes' if is_draft else 'no'  # yes or no
    )
    return entry_xml


__BLOG_SUMMARY_PAGE_ENTRY_TEMPLATE = """本ページは投稿記事一覧です。 (自動更新)

{entry_tree_lines}

※ [自作ツール(Githubリンク)](https://github.com/Symthy/obs-docs-blog-entries-manager) により本ブログへの投稿/更新は自動化
"""


def build_blog_summary_entry_content(entry_tree_lines: str) -> str:
    return __BLOG_SUMMARY_PAGE_ENTRY_TEMPLATE.format(entry_tree_lines=entry_tree_lines)


def get_blog_entry_template() -> str:
    return """[:contents]

{content}
"""


__PHOTO_LIFE_POST_ENTRY_TEMPLATE = """<?xml version="1.0" encoding="utf-8"?>
<entry xmlns="http://purl.org/atom/ns#" xmlns:dc="http://purl.org/dc/elements/1.1/">
  <title>{title}</title>
  <content mode="base64" type="{content_type}">{content}</content>
  <dc:subject>Hatena Blog</dc:subject>
</entry>
"""


def build_photo_entry_post_xml_body(title: str, content_type: str, b64_pic_data: str) -> str:
    entry_xml = __PHOTO_LIFE_POST_ENTRY_TEMPLATE.format(
        title=title,
        content_type=content_type,
        content=b64_pic_data
    )
    return entry_xml
