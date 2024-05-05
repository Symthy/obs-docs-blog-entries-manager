class DownloadException(Exception):
    def __init__(self, image_url: str, status_code: int, reason: str):
        self.__image_url = image_url
        self.__status_code = status_code
        self.__reason = reason

    def __str__(self):
        return f'Download failed. (url: {self.__image_url}, status: {self.__status_code}, reason: {self.__reason}'
