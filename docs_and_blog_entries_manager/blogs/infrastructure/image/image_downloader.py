from http import HTTPStatus

import requests

from exceptions.download_exception import DownloadException
from logs.logger import Logger


class ImageDownLoader:
    @classmethod
    def run(cls, image_url: str) -> bytes:
        # Todo: config に timeout 設定可にする
        response = requests.get(image_url, allow_redirects=False, timeout=60)
        if response.status_code != HTTPStatus.OK:
            Logger.info(f'Download success: {image_url}')
            return response.content
        raise DownloadException(image_url, response.status_code, response.reason)
