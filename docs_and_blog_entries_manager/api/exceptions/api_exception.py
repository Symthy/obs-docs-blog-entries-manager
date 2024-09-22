class ApiException(Exception):
    def __init__(self, method: str, url: str, status_code: int, reason: str, response_body: str | None):
        super().__init__(self.__build_message(method, url, status_code, reason, response_body))

    @staticmethod
    def __build_message(method: str, url: str, status_code: int, reason: str, response_body: str | None):
        req_params = [
            f'api: {method} {url}',
        ]
        res_params = [
            f'status: {status_code}',
            f'reason: {reason}'
        ]
        if response_body is not None and response_body is not '':
            res_params.append(f'body: {response_body}')
        return f'API failed.\n  request:({", ".join(req_params)}\n  response:({", ".join(res_params)}))\n'
