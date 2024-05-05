class ApiException(Exception):
    def __init__(self, method: str, url: str, request_body: str | None, status_code: int, reason: str,
                 response_body: str | None):
        self.__method = method
        self.__url = url
        self.__request_body = request_body
        self.__status_code = status_code
        self.__reason = reason
        self.__response_body = response_body

    def __str__(self):
        req_params = [
            f'api: {self.__method} {self.__url}',
        ]
        if self.__request_body is not None or self.__request_body is not '':
            req_params.append(f'body: {self.__request_body}')
        res_params = [
            f'status: {self.__status_code}',
            f'reason: {self.__reason}'
        ]
        if self.__response_body is not None or self.__response_body is not '':
            res_params.append(f'body: {self.__response_body}')
        return f'API failed.\n  request:({", ".join(req_params)}\n  response:({", ".join(res_params)}))\n'
