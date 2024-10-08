import base64
import hashlib
import random
from datetime import datetime

from config import BlogConfig
from .api_client import BlogApiClient, PhotoApiClient


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
