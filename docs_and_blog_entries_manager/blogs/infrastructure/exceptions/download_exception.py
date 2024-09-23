class DownloadException(Exception):
    def __init__(self, url: str, status_code: int, reason: str):
        super().__init__(f'Failed to download. (url: {url}, status: {status_code}, reason: {reason}')
