from files.value.file_path import FilePath, DirectoryPath

NON_CATEGORY_NAME = 'Others'
SUMMARY_PAGE_TITLE = "Knowledge Stack & Index (全記事一覧)"

LOCAL_STORE_DIR_PATH = './store/'
BLOG_ENTRY_LIST_PATH = FilePath(LOCAL_STORE_DIR_PATH + 'blog_entry_list.json')
DOC_ENTRY_LIST_PATH = FilePath(LOCAL_STORE_DIR_PATH + 'doc_entry_list.json')

CONF_DIR_PATH = './conf/'
DOCS_DIR_PATH = DirectoryPath('./docs/document/')
WORK_DOCS_DIR_PATH = './docs/work/'
EXCLUDE_ENTRY_IDS_TXT_PATH = FilePath(CONF_DIR_PATH + 'exclude_entry_ids.txt')

BLOG_CATEGORY = 'Blog'
