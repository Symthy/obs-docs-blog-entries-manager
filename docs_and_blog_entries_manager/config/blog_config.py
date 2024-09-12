import os
from configparser import ConfigParser

from files.value import FilePath
from libs import ConfigLoader

CONF_SECTION_DEFAULT = 'DEFAULT'
CONF_KEY_HATENA_ID = 'HATENA_ID'
CONF_KEY_BLOG_ID = 'BLOG_ID'
CONF_KEY_API_KEY = 'API_KEY'
CONF_SUMMARY_ENTRY_ID_KEY = 'SUMMARY_ENTRY_ID'
CONF_SUMMARY_ENTRY_TITLE_KEY = 'SUMMARY_ENTRY_TITLE'
CONF_OAUTH_CONSUMER_KEY = 'OAUTH_CONSUMER_KEY'
CONF_OAUTH_CONSUMER_SECRET_KEY = 'OAUTH_CONSUMER_SECRET_KEY'


class BlogConfig:
    def __init__(self, conf: ConfigParser):
        self.__hatena_id = conf.get(CONF_SECTION_DEFAULT, CONF_KEY_HATENA_ID)
        self.__blog_id = conf.get(CONF_SECTION_DEFAULT, CONF_KEY_BLOG_ID)
        self.__api_key = conf.get(CONF_SECTION_DEFAULT, CONF_KEY_API_KEY)
        self.__summary_entry_id = conf.get(CONF_SECTION_DEFAULT, CONF_SUMMARY_ENTRY_ID_KEY)
        self.__summary_entry_title = conf.get(CONF_SECTION_DEFAULT, CONF_SUMMARY_ENTRY_TITLE_KEY)

    @staticmethod
    def load(config_path=FilePath('./conf/blog.conf'.replace('/', os.sep))):
        conf_parser = ConfigLoader()
        with open(config_path.value, 'r', encoding='utf-8') as file:
            conf_parser.read_file(file)
        return BlogConfig(conf_parser)

    @property
    def hatena_id(self):
        return self.__hatena_id

    @property
    def blog_id(self):
        return self.__blog_id

    @property
    def api_key(self):
        return self.__api_key

    @property
    def summary_entry_id(self):
        return self.__summary_entry_id

    @property
    def summary_entry_title(self):
        return self.__summary_entry_title
