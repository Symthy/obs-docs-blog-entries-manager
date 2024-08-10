import base64
import hashlib
import random
from datetime import datetime

from config.blog_config import BlogConfig
from docs_and_blog_entries_manager.api.api_client import ApiClient

HATENA_BLOG_ENTRY_API_URL_TEMPLATE = 'https://blog.hatena.ne.jp/{HATENA_ID}/{BLOG_ID}/atom/entry/'
HATENA_PHOTO_ENTRY_API_URL = 'https://f.hatena.ne.jp/atom/'


class BlogApiClient(ApiClient):
    def __init__(self, hatena_id: str, blog_id: str, base_headers: dict):
        api_url = (HATENA_BLOG_ENTRY_API_URL_TEMPLATE.replace('{HATENA_ID}', hatena_id)
                   .replace('{BLOG_ID}', blog_id))
        super().__init__(api_url, base_headers)


class PhotoApiClient(ApiClient):
    def __init__(self, base_headers: dict):
        super().__init__(HATENA_PHOTO_ENTRY_API_URL, base_headers)


class ApiClientFactory:
    def __init__(self, blog_conf: BlogConfig):
        self.__blog_conf = blog_conf

    def __build_request_header(self) -> dict:
        def __build_wsse(blog_config: BlogConfig):
            user_name = blog_config.hatena_id
            api_key = blog_config.api_key
            created_time = datetime.now().isoformat() + "Z"
            b_nonce = hashlib.sha1(str(random.random()).encode()).digest()
            b_password_digest = hashlib.sha1(b_nonce + created_time.encode() + api_key.encode()).digest()
            wsse = f'UsernameToken Username={user_name}, ' + \
                   f'PasswordDigest={base64.b64encode(b_password_digest).decode()}, ' + \
                   f'Nonce={base64.b64encode(b_nonce).decode()}, ' + \
                   f'Created={created_time}'
            return wsse

        # 'Accept': 'application/xml',
        # 'Content-Type': 'application/xml',
        return {
            'X-WSSE': __build_wsse(self.__blog_conf)
        }

    def build_blog_api_client(self) -> BlogApiClient:
        return BlogApiClient(self.__blog_conf.hatena_id, self.__blog_conf.blog_id, self.__build_request_header())

    def build_photo_api_client(self) -> PhotoApiClient:
        return PhotoApiClient(self.__build_request_header())
