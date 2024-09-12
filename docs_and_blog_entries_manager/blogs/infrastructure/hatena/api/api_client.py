from api import ApiClient

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
