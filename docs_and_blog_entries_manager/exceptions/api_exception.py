class ApiException(Exception):
    def __init__(self, method: str, url: str, body: str | None):
        self.__method = method
        self.__url = url
        self.__body = body

    def __str__(self):
        params = [
            f'api: {self.__method} {self.__url}',
        ]
        if self.__body is not None or self.__body is not '':
            params.append(f'body: {self.__body}')
        return f'API failure. ({", ".join(params)})'
